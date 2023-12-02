      SUBROUTINE d2sDISNC_dxdy_array(E_nu,x,y,OUT,N)
* returns d2sDISNC_dxdy as an array OUT(N), where N = number of entries
      IMPLICIT REAL*8 (A-M,O-Z), INTEGER (N)
      EXTERNAL d2sDISNC_dxdy
      INTEGER I,N
      DIMENSION x(N),y(N),OUT(N)
      DO I = 1, N
        OUT(I) = d2sDISNC_dxdy(E_nu,x(I),y(I))
      END DO
      END SUBROUTINE d2sDISNC_dxdy_array

************************************************************************
      FUNCTION d2sDISNC_dxdy(E_nu,x,y)
************************************************************************
*                                                                      *
*                                                                      *
************************************************************************

         USE PhysMathConstants, ONLY: zero,one,half,mm_Z

         IMPLICIT REAL*8 (A-M,O-Z), INTEGER (N)

         REAL*8 mxl,mxu,myl,myu

         COMMON     /n_NT/n_NT
*        Switch for neutrino type
         COMMON     /n_TT/n_TT
*        Switch for nuclear target type
         COMMON     /n_LP/n_LP
*        Switch for lepton polarization type
         COMMON     /m_ini/m_ini,mm_ini
*        Mass of target nucleon
         COMMON     /m_lep/m_lep,mm_lep
*        Mass of final charged lepton
         COMMON     /n_AG_DIS/n_AG_DIS
*        Switch for model of DIS structure functions
         COMMON     /n_FL_DIS/n_FL_DIS
*        Switch for model of function F_L
         COMMON     /n_RT_DIS/n_RT_DIS
*        Switch for model of function R
         COMMON     /n_Rc_DIS/n_Rc_DIS
*        Switch for model of modification of function R
         COMMON     /n_Qc_DIS/n_Qc_DIS
*        Switch for type of PDF limitation
         COMMON     /n_BF_DIS/n_BF_DIS
*        Switch for type of "bend-factor" for DIS structure functions
         COMMON     /PDFLIB/NGROUP,NSET
*        Parameters for PDFLIB setup
         COMMON     /m_fin/m_fin,mm_fin
*        Mass of final hadron or hadron system
         COMMON     /Q2_DIS/Q2_DIS
*        Minimal Q^2_DIS value for PFDs
         COMMON     /A0_DIS/A0_DIS
*        Parameter in "bend-factor" of DIS structure functions
         COMMON     /B0_DIS/B0_DIS
*        Parameter in "bend-factor" of DIS structure functions
         COMMON     /C0_DIS/C0_DIS
*        Parameter in "bend-factor" of DIS structure functions

         Q2= (2*E_nu)*(m_ini*(x*y))
         CALL W2DIS_lim(E_nu,W2_min,W2_max)
         CALL SFNC(E_nu,x,Q2,F1,F2,F3)

         A1= (x*y)*y
         A2= one-y-(m_ini*(x*y))/(2*E_nu)
         A3= (x*y)*(one-y*half)

         d2sDISNC_dxdy= zero
         dW2= W2_max-W2_min
         IF (dw2>=zero) THEN
           CALL xDIS_lim(E_nu,mxl,mxu)
           IF (x>=mxl .and. x<=mxu) THEN
             CALL yDIS_lim(E_nu,x,myl,myu)
             IF (y>=myl .and. y<=myu) THEN
               d2sDISNC_dxdy= E_nu*(F1*A1+F2*A2+n_NT*F3*A3)/
     #                             (one+Q2/mm_Z)**2
                                      ELSE
               d2sDISNC_dxdy= zero
          endIF
        endIF
      endIF

         RETURN
      END FUNCTION d2sDISNC_dxdy
