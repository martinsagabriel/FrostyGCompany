import argparse
import datetime as dt
import logging
import os
import random as rd
import sys
from time import sleep

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

PAYMENT_METHOD_OPTIONS = [
    ("pix", 0.42),
    ("cartao_credito", 0.33),
    ("cartao_debito", 0.18),
    ("dinheiro", 0.07),
]

ITEM_COUNT_OPTIONS = [
    (1, 0.48),
    (2, 0.26),
    (3, 0.16),
    (4, 0.07),
    (5, 0.03),
]

PRODUCT_SEGMENTS = [
    {"ids": range(1, 9), "weight": 0.32, "max_qty": 2, "mode_qty": 1},
    {"ids": range(9, 17), "weight": 0.28, "max_qty": 4, "mode_qty": 2},
    {"ids": range(17, 25), "weight": 0.22, "max_qty": 6, "mode_qty": 3},
    {"ids": range(25, 33), "weight": 0.18, "max_qty": 3, "mode_qty": 1},
]

SELLER_CLUSTERS = [
    {"start": 1, "end": 300, "weight": 0.28},
    {"start": 301, "end": 1000, "weight": 0.32},
    {"start": 1001, "end": 2000, "weight": 0.22},
    {"start": 2001, "end": 5000, "weight": 0.18},
]

SEASONAL_PRODUCT_BOOST = {
    "morning": {"segment_index": 1, "weight_multiplier": 1.05},
    "afternoon": {"segment_index": 1, "weight_multiplier": 1.0},
    "evening": {"segment_index": 0, "weight_multiplier": 1.08},
    "overnight": {"segment_index": 2, "weight_multiplier": 1.12},
}

HOT_SELLERS = [37, 82, 144, 256, 377, 512, 768, 1024, 2048, 4095]

PRODUCT_OPTIONS = []
SEGMENT_BY_PRODUCT = {}
for segment in PRODUCT_SEGMENTS:
    segment_weight = segment["weight"] / len(segment["ids"])
    for product_id in segment["ids"]:
        PRODUCT_OPTIONS.append((product_id, segment_weight))
        SEGMENT_BY_PRODUCT[product_id] = segment


def setup_logging(quiet: bool) -> None:
    level = logging.WARNING if quiet else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
    )


def env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return float(value)
    except ValueError:
        print(f"Valor inválido para {name}: {value!r}. Usando {default}.", file=sys.stderr)
        return default


def env_int(name: str, default: int | None) -> int | None:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        print(f"Valor inválido para {name}: {value!r}. Usando {default}.", file=sys.stderr)
        return default


def env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate realistic sale events.")
    parser.add_argument(
        "--endpoint",
        default=os.getenv("SALES_ENDPOINT", "http://localhost:3000/sales"),
        help="URL do endpoint de vendas",
    )
    parser.add_argument(
        "--min-delay",
        type=float,
        default=env_float("MIN_DELAY", 0.05),
        help="Tempo mínimo (s) entre ciclos",
    )
    parser.add_argument(
        "--max-delay",
        type=float,
        default=env_float("MAX_DELAY", 0.8),
        help="Tempo máximo (s) entre ciclos",
    )
    parser.add_argument(
        "--max-sales",
        type=int,
        default=env_int("MAX_SALES", None),
        help="Número máximo de vendas a enviar (infinito por padrão)",
    )
    parser.add_argument(
        "--burst",
        type=int,
        default=env_int("BURST_SIZE", 5),
        help="Quantidade de vendas enviadas antes de aguardar o próximo intervalo",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=env_float("REQUEST_TIMEOUT", 5.0),
        help="Timeout em segundos para chamadas HTTP",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Reduz logs no console",
    )
    args = parser.parse_args()
    if args.max_delay < args.min_delay:
        parser.error("--max-delay deve ser maior ou igual a --min-delay")
    if args.burst < 1:
        parser.error("--burst deve ser pelo menos 1")
    if env_bool("QUIET", False):
        args.quiet = True
    return args


def weighted_choice(options):
    total = sum(weight for _, weight in options)
    pick = rd.uniform(0, total)
    cumulative = 0.0
    for value, weight in options:
        cumulative += weight
        if pick <= cumulative:
            return value
    return options[-1][0]


def weighted_sample(options, k):
    pool = list(options)
    result = []
    for _ in range(min(k, len(pool))):
        choice = weighted_choice(pool)
        result.append(choice)
        pool = [(value, weight) for value, weight in pool if value != choice]
    return result


def current_day_period() -> str:
    hour = dt.datetime.utcnow().hour
    if 6 <= hour < 12:
        return "morning"
    if 12 <= hour < 18:
        return "afternoon"
    if 18 <= hour < 24:
        return "evening"
    return "overnight"


def adjust_product_weights(period: str):
    boost = SEASONAL_PRODUCT_BOOST.get(period)
    if not boost:
        return PRODUCT_OPTIONS
    boosted = []
    for product_id, weight in PRODUCT_OPTIONS:
        segment = SEGMENT_BY_PRODUCT[product_id]
        if PRODUCT_SEGMENTS[boost["segment_index"]] is segment:
            boosted.append((product_id, weight * boost["weight_multiplier"]))
        else:
            boosted.append((product_id, weight))
    return boosted


def random_seller_id() -> int:
    if rd.random() < 0.18:
        return rd.choice(HOT_SELLERS)
    cluster = weighted_choice([(c, c["weight"]) for c in SELLER_CLUSTERS])
    return rd.randint(cluster["start"], cluster["end"])


def random_payment_method(period: str) -> str:
    evening_boost = 1.15 if period in {"evening", "overnight"} else 1.0
    adjusted = []
    for method, weight in PAYMENT_METHOD_OPTIONS:
        if method == "pix":
            adjusted.append((method, weight * evening_boost))
        else:
            adjusted.append((method, weight))
    return weighted_choice(adjusted)


def random_quantity(product_id: int) -> int:
    segment = SEGMENT_BY_PRODUCT[product_id]
    left, right = 1, segment["max_qty"]
    mode = segment["mode_qty"]
    sample = rd.triangular(left, right + 0.75, mode)
    return max(1, int(round(sample)))


def build_items(period: str):
    count = weighted_choice(ITEM_COUNT_OPTIONS)
    options = adjust_product_weights(period)
    product_ids = weighted_sample(options, count)
    items = []
    for product_id in product_ids:
        quantity = random_quantity(product_id)
        items.append({"productId": product_id, "quantity": quantity})
    return items


def create_sale_payload(period: str):
    return {
        "sellerId": random_seller_id(),
        "paymentMethod": random_payment_method(period),
        "items": build_items(period),
    }


def create_session() -> requests.Session:
    session = requests.Session()
    adapter = HTTPAdapter(pool_connections=32, pool_maxsize=32, max_retries=Retry(total=3, backoff_factor=0.2, status_forcelist=[500, 502, 503, 504]))
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def random_delay(min_delay: float, max_delay: float) -> float:
    if max_delay <= 0:
        return 0.0
    if max_delay == min_delay:
        return max_delay
    midpoint = (min_delay + max_delay) / 2
    sample = rd.triangular(min_delay, max_delay, midpoint)
    return max(0.0, sample)


def run() -> int:
    args = parse_args()
    setup_logging(args.quiet)
    session = create_session()
    sales_sent = 0
    logging.info("Iniciando envio para %s", args.endpoint)
    try:
        while True:
            period = current_day_period()
            for _ in range(args.burst):
                sale_json = create_sale_payload(period)
                try:
                    response = session.post(args.endpoint, json=sale_json, timeout=args.timeout)
                    response.raise_for_status()
                    logging.debug("Sale enviada com sucesso: seller=%s, itens=%d", sale_json["sellerId"], len(sale_json["items"]))
                except requests.HTTPError as exc:
                    logging.warning("Falha HTTP (%s): %s", exc.response.status_code, exc)
                except requests.RequestException as exc:
                    logging.error("Erro de conexão: %s", exc)
                else:
                    sales_sent += 1
                    if args.max_sales and sales_sent >= args.max_sales:
                        logging.info("Limite de %d vendas atingido", args.max_sales)
                        return 0
            delay = random_delay(args.min_delay, args.max_delay)
            if delay:
                sleep(delay)
    except KeyboardInterrupt:
        logging.info("Encerrado pelo usuário")
    return 0


if __name__ == "__main__":
    sys.exit(run())
