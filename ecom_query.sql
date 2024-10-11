IF OBJECT_ID('tempdb..#stany_SI') IS NOT NULL DROP TABLE #stany_SI;

with tb1 as (
select SymKar, mod, Status, DataWprow, DataKonNowosc
from analizy.dbo.smg_KartotekiTowarowe a 
where pd_czydlasi in (1,2) or Status in ('A9','W3')
), cal as (
select Data
from analizy.dbo.vv_StanyNaDzien
where Logo = 'CDP' and Data >= DATEADD(DAY, -31, GETDATE())
group by Data
), tb2 as (
select *
	,case when (Status in ('A0', 'A1', 'A2', 'A5', 'A6', 'A9', 'A9', 'A10') or (Mod in ('ZC', 'ZA') and Status = 'W7')) and Mod not in ('TR', 'IN') AND dateadd(day,275,DataKonNowosc)>= data then 'NOWOŚĆ'
	when (Status in ('A0', 'A1', 'A2', 'A5', 'A6', 'A9', 'A9', 'A10') or (Mod in ('ZC', 'ZA') and Status = 'W7')) and Mod not in ('TR', 'IN') then 'AKTYWNE'
	else 'NIEAKTYWNE' end StatusZam
from tb1
cross join cal
)
select a.*
, ISNULL(b.Ilosc,0) Stan_Ilosciowy
, ISNULL(b.Wartosc,0) Stan_Wartosciowy
, CASE WHEN b.Ilosc is null then 0 else 1 end Dostepny
, 1 as CNT
into #stany_SI
from tb2 a
	left join (
	select *
	from analizy.dbo.vv_StanyNaDzien
	where Logo = 'CDP' and Data >= DATEADD(DAY, -31, GETDATE())
	) b on a.SymKar = b.SymKar and a.Data = b.Data;

truncate table cf.dbo.ecom_ava_group;

with tb1 as (
	select SymKar, mod, Status, DataWprow, DataKonNowosc, data, StatusZam
	from #stany_SI
	where Data = (select max(data) from #stany_SI)
), tb2 as (
	select symkar, count(*) Dni, SUM(Dostepny) Dostepny 
	from #stany_SI
	group by symkar
), tb3 as (
	select symkar, sum(netto) netto, sum(ilosc) suma_si_ilosc_30 
	from analizy.dbo.wb_rp_sprz_SI_sku 
	where Data >= dateadd(day,-31,GETDATE()) 
	group by symkar
), tb4 as (
select a.*, b.Dni, b.Dostepny, c.netto
, Dni - Dostepny Niedostepny 
, case when suma_si_ilosc_30 <= 0 then 0 else isnull(suma_si_ilosc_30,0) end suma_si_ilosc_30
, case when isnull(suma_si_ilosc_30,0)<=0 then null else (Dni - (Dni - Dostepny))/isnull(suma_si_ilosc_30,0) end schodzenie
, cast(Dostepny as decimal(8,3)) / cast(Dni as decimal(8,3)) dostepnosc
from tb1 a
left join tb2 b on a.SymKar = b.SymKar
left join tb3 c on a.SymKar = c.symkar
), tb5 as (
select SymKar, NTILE(20) OVER(ORDER BY netto DESC) NTIL,
ROW_NUMBER() OVER(ORDER BY suma_si_ilosc_30 DESC, netto DESC) TOP_P
from tb4
where suma_si_ilosc_30 > 0
), tb6 as (
select a.*, b.NTIL, isnull(b.TOP_P, 99999) TOP_P
from tb4 a
LEFT JOIN tb5 b on a.SymKar = b.SymKar
)
insert into cf.dbo.ecom_ava_group
select a.*, b.super_kategoria,
CASE	WHEN NTIL = 1 THEN '5%'
		WHEN NTIL = 2 THEN '10%'
		WHEN NTIL > 2 AND NTIL <= 4 THEN '20%'
		WHEN NTIL > 4 AND NTIL <= 10 THEN '50%'
		WHEN NTIL > 10 THEN '100%'
		ELSE NULL END CENTYL,
CASE	WHEN TOP_P <= 100 THEN 'TOP_100'
		WHEN TOP_P > 100 AND TOP_P <= 500 THEN  'TOP_500'
		WHEN TOP_P > 500 AND TOP_P <= 1000 THEN  'TOP_1000'
		WHEN TOP_P > 1000 AND TOP_P <= 2000 THEN 'TOP_2000'
		ELSE '> TOP_2000' END RANKING
from tb6 a
left join analizy.dbo.vv_SuperKategoria b on a.Mod = b.mod;

truncate table cf.dbo.ecom_ava_daily;
with tb1 as (
select *
from #stany_SI
where data = (select max(data) from #stany_SI)
)
insert into cf.dbo.ecom_ava_daily
select a.Data, a.mod, a.StatusZam, b.CENTYL, b.RANKING, b.super_kategoria, sum(Stan_Ilosciowy) Stan_Ilosciowy, sum(Stan_Wartosciowy) Stan_Wartosciowy, sum(a.Dostepny) Dostepny, sum(a.CNT) CNT
from tb1 a
left join cf.dbo.ecom_ava_group b on a.symkar = b.symkar
group by a.Data, a.mod, a.StatusZam, b.CENTYL, b.RANKING, b.super_kategoria
