> 检索摘要：2.61 Internal Combustion Engines（Spring 2017，Graduate）的「Related Resources」。页内标题：Related Resources；Main program to call exhaust_compo and plots results: exhaust_compo_main.m；Function subroutine to calculate the composition: exhaust_compo.m。分隔线后是该页英文原文，未翻译、未改写。

- Source: https://ocw.mit.edu/courses/2-61-internal-combustion-engines-spring-2017/pages/related-resources/
- source_format: html
- capture_date: 2026-10-03
- license: https://creativecommons.org/licenses/by-nc-sa/4.0/

---
## Related Resources

This page contains engine performance specifications and scripts for determining engine exhaust composition.

[Engine Performance Specifications (XLSX)](https://ocw.mit.edu/courses/2-61-internal-combustion-engines-spring-2017/resources/engine_specs/)

#### Main program to call exhaust_compo and plots results: exhaust_compo_main.m

```
%main driver for exhaust_compo %Gasoline CHmOn; m= 1.87 ;n= 0 ; Lambda=[ 0.6 : 0.1 : 1.4 ]; [xco2,xh2o,xco,xh2,xo2,xn2]=exhaust_compo(m,n,Lambda); h=plot(Lambda,[xco2,xh2o,xco,xh2,xo2], '-' ); xlabel( '\lambda' ); ylabel( 'Exhaust Mole fractions' ); legend( 'CO2' , 'H2O' , 'CO' , 'H2' , 'O2' );
```

#### Function subroutine to calculate the composition: exhaust_compo.m

```
function [xco2,xh2o,xco,xh2,xo2,xn2]= exhaust_compo (m,n,Lambda); %calculate xhaust mole fractions %For lean to stoichiometric combustion, assume complete burning %For rich combustion, assume water gas equilibrium constant k=3.7 %Input: m,n are the hydrogen and oxygen to carbon ratios of the fuel %Input: Lambda is the column vector of air equivalence ratio %Output are the mole fractions of the exhaust composition k= 3.7 ; nL= length (Lambda); xco2= zeros (nL, 1 ); xco= zeros (nL, 1 ); xh2o= zeros (nL, 1 ); xh2= zeros (nL, 1 ); xo2= zeros (nL, 1 ); xn2= zeros (nL, 1 ); for i = 1 :nL; L=Lambda( i ); if (L < = 0 );error( 'Lambda must be positive' ); end ; if (L > = 1 ); %=============== Lambda >=1 ================== z= 1 + 0.25 m - 0.5 n; Lm1=L - 1 ; co= 0 ;h2= 0 ;co2= 1 ;h2o= 0.5 m; n2=z3. 773 L; o2=Lm1z; else ; %=============== Lambda < 1 ================== z=n( 1 - L) + 2 L( 1 + 0.25 m); B= 2 + ( 0.5 m - 1 )k - ( 1 - k)z; A= 0.5 m( 1 - k); C=k( 1 - z); b=( - B + sqrt (B.B - 4 AC)) / ( 2 A); a=b ./ (k + ( 1 - k)b); co2=a; co= 1 - a; h2o= 0.5 mb; h2= 0.5 m( 1 - b); n2=( 1 + 0.25 m - 0.5 n) 3.773 * L; o2= 0 ; end %============================================= total=co + h2 + co2 + h2o + n2 + o2; xco( i )=co ./ total; xh2( i )=h2 ./ total; xco2( i )=co2 ./ total; xh2o( i )=h2o ./ total; xo2( i )=o2 ./ total; xn2( i )=n2 ./ total; end
```
