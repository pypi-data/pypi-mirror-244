      SUBROUTINE d2sDISCC_dxdy_array(E_nu,x,y,OUT,N)
* returns d2sDISCC_dxdy as an array OUT(N), where N = number of entries
      IMPLICIT REAL*8 (A-M,O-Z), INTEGER (N)
      EXTERNAL d2sDISCC_dxdy
      INTEGER I,N
      DIMENSION x(N),y(N),OUT(N)
      DO I = 1, N
        OUT(I) = d2sDISCC_dxdy(E_nu,x(I),y(I))
      END DO
      END SUBROUTINE d2sDISCC_dxdy_array

************************************************************************
      FUNCTION d2sDISCC_dxdy(E_nu,x,y)
************************************************************************
*                                                                      *
*     This FUNCTION returns the charged current double differenti-     *
*     alneutrino-nucleon cross section  $d^2\sigam^CC_DIS/(dx dy)$     *
*     for  (anti)neutrino-nucleon  deep inelastic scattering. Here     *
*     Fi are parton structure functions of target nucleon,  Ai are     *
*     dynamic factors  and Ei are from the  $~(q^\mu q^\nu)/M^2_W$     *
*     part of the massive boson  propagator according to Ref. [1].     *
*                                                                      *
*     REFERENCES                                                       *
*                                                                      *
*     [1] S. Kretzer,  M.H. Reno.  "Tau  neutrino  deep  inelastic     *
*         charged  current  interactions,"  Phys. Rev. D 66 (2002)     *
*         113007 [arXiv: hep-ph/0208187].                              *
*     [2] K.S. Kuzmin, "Neutrino scattering off nucleons and pola-     *
*         rization of charged leptons in  quasielastic reactions,"     *
*         Ph.D. Thesis, JINR, Dubna, 2009/04/01  (Ph.D. Thesis ad-     *
*         visor V.A. Naumov, BLTP JINR).                               *
*                                                                      *
************************************************************************

         USE PhysMathConstants, ONLY: zero,one,half,mm_W

         IMPLICIT REAL*8 (A-M,O-Z), INTEGER (N)

         REAL*8 mxl,mxu,myl,myu

         COMMON     /n_NT/n_NT
*         Switch for neutrino type
         COMMON     /n_TT/n_TT
*         Switch for nuclear target type
         COMMON     /n_LP/n_LP
*         Switch for lepton polarization type
         COMMON     /m_ini/m_ini,mm_ini
*         Mass of target nucleon
         COMMON     /m_lep/m_lep,mm_lep
*         Mass of final charged lepton
         COMMON     /n_AG_DIS/n_AG_DIS
*         Switch for model of DIS structure functions
         COMMON     /n_FL_DIS/n_FL_DIS
*         Switch for model of function F_L
         COMMON     /n_RT_DIS/n_RT_DIS
*         Switch for model of function R
         COMMON     /n_Rc_DIS/n_Rc_DIS
*         Switch for model of modification of function R
         COMMON     /n_Qc_DIS/n_Qc_DIS
*         Switch for type of PDF limitation
         COMMON     /n_BF_DIS/n_BF_DIS
*         Switch for type of "bend-factor" for DIS structure functions
         COMMON     /PDFLIB/NGROUP,NSET
*         Parameters for PDFLIB setup
         COMMON     /m_fin/m_fin,mm_fin
*         Mass of final hadron or hadron system
         COMMON     /Q2_DIS/Q2_DIS
*         Minimal Q^2_DIS value for PFDs
         COMMON     /A0_DIS/A0_DIS
*         Parameter in "bend-factor" of DIS structure functions
         COMMON     /B0_DIS/B0_DIS
*         Parameter in "bend-factor" of DIS structure functions
         COMMON     /C0_DIS/C0_DIS
*         Parameter in "bend-factor" of DIS structure functions

         d2DISCC_dxdy=0
         Q2= 2*m_ini*x*y*E_nu
         CALL W2DIS_lim(E_nu,W2_min,W2_max)
         CALL SFCC(E_nu,x,Q2,F1,F2,F3,F4,F5,F6)
*        1+(m_lep/m_W)**2*(1+((Q2/mm_W)/2))
         E1= 1
*        1+(m_lep/m_W)**2*y*(1+y*(Q2+mm_lep)/(4*mm_W))*(1-y-(Q2+mm_lep)/(2*E_nu)**2)
         E2= 1
*        1+(Q2/mm_W)*(1+((Q2/mm_W)/2))*2
         E4= 1
*        1+(Q2/mm_W)+(y/2)*(1+(Q2/mm_W))*((m_lep/m_W)**2+(Q2/mm_W))
         E5= 1

         a= mm_lep/(2*m_ini*E_nu)
         IF (n_LP.eq.0) THEN
           GOTO 1
                        ELSE
           E_lep= (one-y)*E_nu
           IF (E_lep**2-mm_lep.gt.zero) THEN
             P_lep= sqrt(E_lep**2-mm_lep)
                                        ELSE
             P_lep= E_lep*(one-mm_lep/(2*E_lep**2))
        endIF
           p= (x*y)+a*(one-(2*E_nu)/(E_lep+P_lep)       )
           m= (x*y)+a*(one-(2*E_nu)*(E_lep+P_lep)/mm_lep)
           IF (n_NT.eq.1) THEN
             IF (n_LP.eq.1) THEN; GOTO 2
                            ELSE; GOTO 3
             endIF
                          ELSE
             IF (n_LP.eq.1) THEN; GOTO 3
                            ELSE; GOTO 2
          endIF
        endIF
      endIF
*        ------------------------------------------------------------- *
*        NO POLARIZATION                                               *
*        ------------------------------------------------------------- *
    1    f = E_nu
         A1= y*((x*y)+a)
         A2= one-y-m_ini*(x*y)/(2*E_nu)-(m_lep/(2*E_nu))**2
         A3= y*(x*(one-y*half)-a*half)
         A4= a*((x*y)+a)
         A5=-a
         GOTO 4
*        ------------------------------------------------------------- *
*        "CORRECT" POLARIZATION                                        *
*        ------------------------------------------------------------- *
    2    f = E_nu*(E_lep+P_lep)/(2*P_lep)
         A1= p*y
         A2= (one-p*m_ini/(2*P_lep))*P_lep/E_nu
         A3= p*(E_nu+P_lep)/(2*E_nu)
         A4=-m*(mm_lep/ (E_lep+P_lep))**2/((2*E_nu)*m_ini)
         A5= m* mm_lep/((E_lep+P_lep)    * (2*E_nu)      )
         GOTO 4
*        ------------------------------------------------------------- *
*        "UNCORRECT" POLARIZATION                                      *
*        ------------------------------------------------------------- *
    3    f = E_nu*mm_lep/(2*(E_lep+P_lep)*P_lep)
         A1=-m*y
         A2= (one+m*m_ini/(2*P_lep))*P_lep/E_nu
         A3=-m*(E_nu -P_lep)   / (2*E_nu)
         A4= p*(E_lep+P_lep)**2/((2*E_nu)*m_ini)
         A5=-p*(E_lep+P_lep)   / (2*E_nu)
*        ------------------------------------------------------------- *

    4    dW2= W2_max-W2_min
         IF (dW2<zero) THEN
           d2sDISCC_dxdy= zero
                       ELSE
           CALL xDIS_lim(E_nu,mxl,mxu)
           IF (x<mxl .or. x>mxu) THEN
             d2sDISCC_dxdy= zero
                                 ELSE
            CALL yDIS_lim(E_nu,x,myl,myu)
            IF (y>=myl .and. y<=myu) THEN
              d2sDISCC_dxdy= f*(F1*A1*E1+F2*A2*E2+
     #                          n_NT*F3*A3+F4*A4*E4+F5*A5*E5)/
     #                         (one+(Q2/mm_W))**2
                                     ELSE
              d2sDISCC_dxdy= zero
         endIF
       endIF
      endIF
         RETURN
      END FUNCTION d2sDISCC_dxdy
