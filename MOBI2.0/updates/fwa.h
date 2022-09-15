!======================== include file "fwa.h" =========================

!      parameters for adding anomalous fresh water pulses

!      isfwa1     = starting i index of section 1 for freshwater
!      iefwa1     = ending i index of section 1 for freshwater
!      isfwa2     = starting i index of section 2 for freshwater
!      iefwa2     = ending i index of section 2 for freshwater
!      jsfwa1     = starting j index of section 1 for freshwater
!      jefwa1     = ending j index of section 1 for freshwater
!      jsfwa2     = starting j index of section 2 for freshwater
!      jefwa2     = ending j index of section 2 for freshwater
!      mrfwa      = regional mask region for freshwater
!      fwaflxi1   = initial fresh water flux for section 1 (Sv)
!      fwaflxi2   = initial fresh water flux for section 2 (Sv)
!      fwayri1    = year to start fresh water flux section 1
!      fwayrf1    = year to end fresh water flux section 1
!      fwayri2    = year to start fresh water flux section 2
!      fwayrf2    = year to end fresh water flux section 2
!      fwarate1    = rate of increase in flux (Sv year-1)
!      fwarate2    = rate of increase in flux (Sv year-1)
!      areafwa1    = area of fresh water anomaly
!      areafwc1    = area of fresh water compensation
!      areafwa2    = area of fresh water anomaly
!      areafwc2    = area of fresh water compensation
!      compensate = flag to compensate for flux everywhere else
!      fwawt      = weighting for fresh water anomaly area
!      fwcwt      = weighting for fresh water compensation area

       integer isfwa1, iefwa1, jsfwa1, jefwa1, mrfwa
       integer isfwa2, iefwa2, jsfwa2, jefwa2
       common /fwa_i/ isfwa1, iefwa1, jsfwa1, jefwa1
       common /fwa_i/ isfwa2, iefwa2, jsfwa2, jefwa2
       common /fwa_i/ mrfwa

       logical compensate
       common /fwa_l/ compensate

       real fwaflxi1, fwayri1, fwayrf1, fwarate1, areafwa1, areafwc1
       real fwaflxi2, fwayri2, fwayrf2, fwarate2, areafwa2, areafwc2
       real fwawt1, fwcwt1
       real fwawt2, fwcwt2
       real rand1, rand11, rand12, rand13, previous_time, randamp1
       real rand2, rand21, rand22, rand23, randamp2
       common /fwa_r/ fwaflxi1, fwayri1, fwayrf1, fwarate1
       common /fwa_r/ fwaflxi2, fwayri2, fwayrf2, fwarate2
       common /fwa_r/ areafwa1, areafwc1
       common /fwa_r/ areafwa2, areafwc2
       common /fwa_r/ fwawt1(imt,jmt), fwcwt1(imt,jmt)
       common /fwa_r/ fwawt2(imt,jmt), fwcwt2(imt,jmt)
       common /fwa_r/ rand1, rand11, rand12, rand13, randamp1
       common /fwa_r/ rand2, rand21, rand22, rand23, randamp2
       common /fwa_r/ previous_time
