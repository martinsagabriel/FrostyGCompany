select 
	s.saledate,
	s.paymentmethod,
	p.productname,
	p2.categoryname,
	si.quantity, 
	p.unitprice,
	p.unitprice * si.quantity as totalvalue,
	s2.employeecode,
	s3.storeid,
	s3.city,
	s3.state,
	concat(s3.latitude, ',', s3.longitude) as storelocation
from sale s 
inner join saleitem si on si.saleid  = s.saleid 
inner join product p on si.productid = p.productid
inner join seller s2 on s.sellerid = s2.sellerid
inner join store s3 on s2.storeid = s3.storeid
inner join productcategory p2 on p2.categoryid = p.categoryid 


select 
	date(s.saledate) as data,
	sum(si.quantity) as qtdproducts,
	sum(p.unitprice * si.quantity) as totalvalue
from sale s 
inner join saleitem si on si.saleid  = s.saleid 
inner join product p on si.productid = p.productid
group by date(s.saledate) 


	

	