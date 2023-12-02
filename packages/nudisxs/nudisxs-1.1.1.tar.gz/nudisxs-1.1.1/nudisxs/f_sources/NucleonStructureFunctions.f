************************************************************************
*      SUBROUTINE NucleonStructureFunctions(E_nu,x_B,Q2,
*     #                                     F1,F2,F3,F4,F5,F6)
       SUBROUTINE INITPDF(PDFNAME)
************************************************************************
*                                                                      *
*                                                                      *
*     REFERENCES                                                       *
*                                                                      *
*     [1] E.A. Paschos and J.Y. Yu,  "Neutrino interactions in os-     *
*         cillation  experiments,"  Phys. Rev. D 65 (2002) 033002.     *
*     [2] K.S. Kuzmin, "Neutrino scattering off nucleons and pola-     *
*         rization of  charged leptons in quasielastic reactions,"     *
*         Ph.D. Thesis, JINR, Dubna, 2009/04/01  (Ph.D. Thesis ad-     *
*         visor V.A. Naumov, BLTP JINR).                               *
*     [3] A. Bodek and U.K. Yang, ","
*     [4] V.A. Naumov, Privite communications, 2006 - 2007.            *
*     [5] U.K. Yang, "A measurement of differential cross sections in  *
*         charged current neutrino interactions  on iron and a global  *
*         structure functions analysis", Ph. D. Thesis, University of  *
*         Rochester, Rochester, New York, 2001; FERMILAB-THESIS-2001-  *
*         09, 2001.                                                    *
*                                                                      *
*                      A.I. Alikhanov ITEP, Moscow, Russia 2005/06/17  *
************************************************************************

         USE PhysMathConstants

         IMPLICIT REAL*8 (A-M,O-Z), INTEGER (N)
         CHARACTER(64) PDFNAME

         SAVE

         REAL*8,PARAMETER::
     #        N_SLAC        = 1.011,
     #        A_BY          = 0.418,
     #        B_BY          = 0.222,
     #        C_BY          = 0.178,
     #        mm_cBY        = 1.5**2,
     #        C_D           = 0.710,
     #        C1_val        = 0.604,
     #        C2_val        = 0.485,
     #        C_sea         = 0.381,
*             g ^2_L + g ^2_R
     #        g2_0LRp       = ( 0.5-2*sin2W/3)**2+(-2*sin2W/3)**2,
*             g'^2_L + g'^2_R
     #        g2_1LRp       = (-0.5+1*sin2W/3)**2+( 1*sin2W/3)**2,
*             g ^2_L - g ^2_R
     #        g2_0LRm       = ( 0.5-2*sin2W/3)**2-(-2*sin2W/3)**2,
*             g'^2_L - g'^2_R
     #        g2_1LRm       = (-0.5+1*sin2W/3)**2-( 1*sin2W/3)**2,
     #        m_X_CqDq_nu_p = m_Spp_c,
     #        m_X_CqSq_nu_p = m_p+m_Dsm,
     #        m_X_CqSq_nu_n = m_n+m_Dsm,
     #        m_X_CqDa_an_p = m_p+m_Dpm,
     #        m_X_CqSa_an_p = m_p+m_Dsm,
     #        m_X_CqSa_an_n = m_n+m_Dsm,
     #        mm_X_CqDq_nu_p= m_X_CqDq_nu_p**2,
     #        mm_X_CqSq_nu_p= m_X_CqSq_nu_p**2,
     #        mm_X_CqSq_nu_n= m_X_CqSq_nu_n**2,
     #        mm_X_CqDa_an_p= m_X_CqDa_an_p**2,
     #        mm_X_CqSa_an_p= m_X_CqSa_an_p**2,
     #        mm_X_CqSa_an_n= m_X_CqSa_an_n**2

         COMMON       /n_NT/n_NT
*        Switch for neutrino type
         COMMON       /n_TT/n_TT
*        Switch for nuclear target type
         COMMON   /n_AG_DIS/n_AG_DIS
*        Switch for model of DIS structure functions
         COMMON   /n_FL_DIS/n_FL_DIS
*        Switch for model of function F_L
         COMMON   /n_Rc_DIS/n_Rc_DIS
*        Switch for model of modification of function R
         COMMON   /n_Qc_DIS/n_Qc_DIS
*        Switch for type of PDF limitation
         COMMON     /PDFLIB/NGROUP,NSET
*        Parameters for PDFLIB setup
         COMMON      /m_ini/m_ini,mm_ini
*        Mass of target nucleon
         COMMON      /m_lep/m_lep,mm_lep
*        Mass of final charged lepton
         COMMON     /Q2_DIS/Q2_DIS
*        Minimal Q^2_DIS value for PFDs
         COMMON     /A0_DIS/A0_DIS
*        Parameter in "bend-factor" of DIS structure functions
         COMMON     /B0_DIS/B0_DIS
*        Parameter in "bend-factor" of DIS structure functions
         COMMON     /C0_DIS/C0_DIS
*        Parameter in "bend-factor" of DIS structure functions

         DIMENSION f(-6:6)

*        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*        PREVIOUS METHOD BASED ON CERN PDFLIB LIBRARY
*        CALL PDFsetup(E_nu,x_B,Q2,Uq,Ua,Dq,Da,Sq,Sa,Cq,Ca)
*        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*        CURRENT METHOD BASED ON LHAPDF PACKAGE
         CALL InitPDFsetByName(PDFNAME)
*        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *

         RETURN

*     ==================================================================
*     x_Bjorken
      ENTRY SFCC(E_nu,x_B,Q2,F1,F2,F3,F4,F5,F6)
*     ==================================================================
         IF (n_Qc_DIS.eq.0 .and. Q2.lt.Q2_DIS) THEN
*          x rescaling
           x_r= x_B*Q2_DIS/Q2
*          x Nachtmann+rescaling
           x_0= 2*x_r/(1+sqrt(1+4*mm_ini*x_r**2/Q2))
                                               ELSE
*          x Nachtmann
           x_0= 2*x_B/(1+sqrt(1+4*mm_ini*x_B**2/Q2))
      endIF
*        x Feynman
         x_c= x_0*(1+mm_c/Q2)

         SELECTCASE(n_AG_DIS)
*              ======================================================= *
               CASE(       0)
*              E.A. Paschos and J.Y. Yu, Ref. [1]
*              ======================================================= *
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*              PREVIOUS METHOD BASED ON CERN PDFLIB LIBRARY
*              CALL PDF(E_nu,x_B,Q2,
*    #                  Uq_0,Ua_0,Dq_0,Da_0,Sq_0,Sa_0,Cq_0,Ca_0,G,A)
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*              CURRENT METHOD BASEN ON LHAPDF PACKAGE
               CALL evolvePDF(x_B,sqrt(Q2),f)
               Uq_0= f(+2); Dq_0= f(+1); Sq_0= f(+3); Cq_0= f(+4)
               Ua_0= f(-2); Da_0= f(-1); Sa_0= f(-3); Ca_0= f(-4)

*               write(*,*) x_B,sqrt(Q2),f
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*              ------------------------------------------------------- *
*              NON-CHARM PRODUCTION COMPONENTS                         *
*              ------------------------------------------------------- *
               SELECTCASE(n_TT)
                     CASE(   1)
                     SELECTCASE(n_NT)
                           CASE(   1)
*                          \nu + p
                           F2_0= 2*x_B*(Dq_0*c2C+Sq_0*s2C+Ua_0+Ca_0)
                           F3_0= 2    *(Dq_0*c2C+Sq_0*s2C-Ua_0-Ca_0)
                           CASE(  -1)
*                          \overline{\nu} + p
                           F2_0= 2*x_B*(Uq_0*c2C+Cq_0*s2C+Da_0+Sa_0)
                           F3_0= 2    *(Uq_0*c2C+Cq_0*s2C-Da_0-Sa_0)
                  endSELECT
                     CASE(   2)
                     SELECTCASE(n_NT)
                           CASE(   1)
*                          \nu + n
                           F2_0= 2*x_B*(Uq_0*c2C+Sq_0*s2C+Da_0+Ca_0)
                           F3_0= 2    *(Uq_0*c2C+Sq_0*s2C-Da_0-Ca_0)
                           CASE(  -1)
*                          \overline{\nu} + n
                           F2_0= 2*x_B*(Dq_0*c2C+Cq_0*s2C+Ua_0+Sa_0)
                           F3_0= 2    *(Dq_0*c2C+Cq_0*s2C-Ua_0-Sa_0)
                  endSELECT
            endSELECT
               F1_0= F2_0/(2*x_B)
               F4_0=(F2_0/(2*x_B)-F1_0)/(2*x_B)
               F5_0= F2_0/x_B
*              ------------------------------------------------------- *
*              CHARM PRODUCTION COMPONENTS                             *
*              ------------------------------------------------------- *
               IF (x_c.ge.one) THEN
                 F1_c= zero
                 F2_c= zero
                 F3_c= zero
                 F4_c= zero
                 F5_c= zero
                               ELSE
*                - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*                PREVIOUS METHOD BASED ON CERN PDFLIB LIBRARY
*                CALL PDF(E_nu,x_c,Q2,
*    #                    Uq,Ua,Dq_c,Da_c,Sq_c,Sa_c,Cq,Ca,G,A)
*                - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*                CURRENT METHOD BASEN ON LHAPDF PACKAGE
                 CALL evolvePDF(x_c,sqrt(Q2),f)
                 Uq  = f(+2); Dq_c= f(+1); Sq_c= f(+3); Cq  = f(+4)
                 Ua  = f(-2); Da_c= f(-1); Sa_c= f(-3); Ca  = f(-4)
*                - - - - - - - - - - - - - - - - - - - - - - - - - - - *
                 SELECTCASE(n_TT)
                       CASE(   1)
                       SELECTCASE(n_NT)
                             CASE(   1)
*                            \nu + p
                             F2_c= 2*x_B*(Dq_c*s2C+Sq_c*c2C)
                             F3_c= 2*    (Dq_c*s2C+Sq_c*c2C)
                             CASE(  -1)
*                            \overline{\nu} + p
                             F2_c= 2*x_B*(Uq_0*s2C+Cq_0*c2C)
                             F3_c= 2*    (Uq_0*s2C+Cq_0*c2C)
                    endSELECT
                       CASE(   2)
                       SELECTCASE(n_NT)
                             CASE(   1)
*                            \nu + n
                             F2_c= 2*x_B*(Uq_0*s2C+Sq_c*c2C)
                             F3_c= 2*    (Uq_0*s2C+Sq_c*c2C)
                             CASE(  -1)
*                            \overline{\nu} + n
                             F2_c= 2*x_B*(Dq_c*s2C+Cq_0*c2C)
                             F3_c= 2*    (Dq_c*s2C+Cq_0*c2C)
                    endSELECT
              endSELECT
                 F1_c= F2_c/(2*x_B)
                 F4_c= zero
                 F5_c= zero
            endIF
*              ------------------------------------------------------- *
*              ======================================================= *
               CASE(       1)
*              V.A. Naumov and K.S. Kuzmin, Ref.[2]
*              ======================================================= *
*              ------------------------------------------------------- *
*              NON-CHARM PRODUCTION COMPONENTS                         *
*              ------------------------------------------------------- *
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*              PREVIOUS METHOD BASED ON CERN PDFLIB LIBRARY
*              CALL PDF(E_nu,x_0,Q2,
*    #                  Uq_0,Ua_0,Dq_0,Da_0,Sq_0,Sa_0,Cq_0,Ca_0,G,A)
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*              CURRENT METHOD BASEN ON LHAPDF PACKAGE
               CALL evolvePDF(x_0,sqrt(Q2),f)
               Uq_0= f(+2); Dq_0= f(+1); Sq_0= f(+3); Cq_0= f(+4)
               Ua_0= f(-2); Da_0= f(-1); Sa_0= f(-3); Ca_0= f(-4)
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*              OUTPUT TEST INFORMATION
*              write(6,*) 'nucleonstruct'
*              write(6,*) E_nu,x_0,Q2,Uq_0,Ua_0
*              write(6,*) Dq_0,Da_0,Sq_0,Sa_0,Cq_0,Ca_0,G,A
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
               SELECTCASE(n_TT)
                     CASE(   1)
                     SELECTCASE(n_NT)
                           CASE(   1)
*                          \nu + p
                           F2_0= 2*x_B*(Dq_0*c2C+Sq_0*s2C+Ua_0+Ca_0)
                           F3_0= 2    *(Dq_0*c2C+Sq_0*s2C-Ua_0-Ca_0)
                           CASE(  -1)
*                          \overline{\nu} + p
                           F2_0= 2*x_B*(Uq_0*c2C+Cq_0*s2C+Da_0+Sa_0)
                           F3_0= 2    *(Uq_0*c2C+Cq_0*s2C-Da_0-Sa_0)
                  endSELECT
                     CASE(   2)
                     SELECTCASE(n_NT)
                           CASE(   1)
*                          \nu + n
                           F2_0= 2*x_B*(Uq_0*c2C+Sq_0*s2C+Da_0+Ca_0)
                           F3_0= 2    *(Uq_0*c2C+Sq_0*s2C-Da_0-Ca_0)
                           CASE(  -1)
*                          \overline{\nu} + n
                           F2_0= 2*x_B*(Dq_0*c2C+Cq_0*s2C+Ua_0+Sa_0)
                           F3_0= 2    *(Dq_0*c2C+Cq_0*s2C-Ua_0-Sa_0)
                  endSELECT
            endSELECT
               F2_0= F2_0*BendFactor(Q2,A0_DIS,B0_DIS,C0_DIS)

               FL_0= F0_L(E_nu,x_0,Q2,F2_0)
               F1_0=(F2_0*(1+4*mm_ini*x_B**2/Q2)-FL_0)/(2*x_B)
               F4_0=(F2_0/(2*x_B)-F1_0)/(2*x_B)
               F5_0= F2_0/x_B
*              ------------------------------------------------------- *
*              CHARM PRODUCTION COMPONENTS                             *
*              ------------------------------------------------------- *
               IF (x_c.ge.one) THEN
                 F1_c= zero
                 F2_c= zero
                 F3_c= zero
                 F4_c= zero
                 F5_c= zero
                               ELSE
*                - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*                PREVIOUS METHOD BASED ON CERN PDFLIB LIBRARY
*                CALL PDF(E_nu,x_c,Q2,
*    #                    Uq,Ua,Dq_c,Da_c,Sq_c,Sa_c,Cq,Ca,G,A)
*                - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*                CURRENT METHOD BASEN ON LHAPDF PACKAGE
                 CALL evolvePDF(x_c,sqrt(Q2),f)
                 Uq  = f(+2); Dq_c= f(+1); Sq_c= f(+3); Cq  = f(+4)
                 Ua  = f(-2); Da_c= f(-1); Sa_c= f(-3); Ca  = f(-4)
*                - - - - - - - - - - - - - - - - - - - - - - - - - - - *
                 SELECTCASE(n_TT)
                       CASE(   1)
                       SELECTCASE(n_NT)
                             CASE(   1)
*                            \nu + p
                             IF (x_B       .le.
     #                           one/(1+(mm_X_CqSq_nu_p-mm_p)/Q2).and.
     #                           2*m_p*E_nu.ge.
     #                           (m_lep+m_X_CqSq_nu_p)**2-mm_p)
     #                                                             THEN
                               F2_c= 2*x_B*(Dq_c*s2C+Sq_c*c2C)
                               F3_c= 2*    (Dq_c*s2C+Sq_c*c2C)
                         ELSEIF (x_B       .le.
     #                           one/(1+(mm_X_CqDq_nu_p-mm_p)/Q2).and.
     #                           2*m_p*E_nu.ge.
     #                           (m_lep+m_X_CqDq_nu_p)**2-mm_p)
     #                                                             THEN
                               F2_c= 2*x_B*(Dq_c*s2C)
                               F3_c= 2*    (Dq_c*s2C)
                                                                   ELSE
                               F2_c= zero
                               F3_c= zero
                          endIF
                             CASE(  -1)
*                            \overline{\nu} + p
                             IF (x_B       .le.
     #                           one/(1+(mm_X_CqSa_an_p-mm_p)/Q2).and.
     #                           2*m_p*E_nu.ge.
     #                           (m_lep+m_X_CqSa_an_p)**2-mm_p)
     #                                                             THEN
                               F2_c= 2*x_B*
     #                               (Uq_0*s2C+Cq_0*c2C+(Da_c-Da_0)*s2C+
     #                                                  (Sa_c-Sa_0)*c2C)
                               F3_c= 2*
     #                               (Uq_0*s2C+Cq_0*c2C-(Da_c-Da_0)*s2C-
     #                                                  (Sa_c-Sa_0)*c2C)
                         ELSEIF (x_B       .le.
     #                           one/(1+(mm_X_CqDa_an_p-mm_p)/Q2).and.
     #                           2*m_p*E_nu.ge.
     #                           (m_lep+m_X_CqDa_an_p)**2-mm_p)
     #                                                             THEN
                               F2_c= 2*x_B*
     #                               (Uq_0*s2C+Cq_0*c2C+(Da_c-Da_0)*s2C)
                               F3_c= 2*
     #                               (Uq_0*s2C+Cq_0*c2C-(Da_c-Da_0)*s2C)
                                                                   ELSE
                               F2_c= zero
                               F3_c= zero
                          endIF
                    endSELECT
                       CASE(   2)
                       SELECTCASE(n_NT)
                             CASE(   1)
*                            \nu + n
                             IF (x_B       .le.
     #                           one/(1+(mm_X_CqSq_nu_n-mm_n)/Q2).and.
     #                           2*m_n*E_nu.ge.
     #                           (m_lep+m_X_CqSq_nu_n)**2-mm_n)
     #                                                             THEN
                               F2_c= 2*x_B*(Uq_0*s2C+Sq_c*c2C)
                               F3_c= 2*    (Uq_0*s2C+Sq_c*c2C)
                                                                   ELSE
                               F2_c= zero
                               F3_c= zero
                          endIF
                             CASE(  -1)
*                            \overline{\nu} + n
                             IF (x_B       .le.
     #                           one/(1+(mm_X_CqSa_an_n-mm_n)/Q2).and.
     #                           2*m_n*E_nu.ge.
     #                           (m_lep+m_X_CqSa_an_n)**2-mm_n)
     #                                                             THEN
                               F2_c= 2*x_B*
     #                               (Dq_0*s2C+Cq_0*c2C+(Sa_c-Sa_0)*c2C)
                               F3_c= 2*
     #                               (Dq_0*s2C+Cq_0*c2C-(Sa_c-Sa_0)*c2C)
                                                                   ELSE
                               F2_c= zero
                               F3_c= zero
                          endIF
                    endSELECT
              endSELECT
                 F2_c= F2_c*BendFactor(Q2,A0_DIS,B0_DIS,C0_DIS)
                 SELECTCASE(n_Rc_DIS)
                       CASE(       0)
                       FL_c= F0_L(E_nu,x_0,    Q2,F2_c)
                       CASE(       1)
                       FL_c= Fc_L(E_nu,x_0,x_c,Q2,F2_c)
              endSELECT
                 F1_c= (F2_c*(1+4*mm_ini*x_B**2/Q2)-FL_c)/(2*x_B)
                 F4_c= zero
                 F5_c= zero
            endIF
*              ------------------------------------------------------- *
*              ======================================================= *
               CASE(       2)
*              A. Bodek and U.K. Yang, Ref. [3]
*              ======================================================= *
               IF (NGROUP.ne.5 ) STOP 'CASE FOR GRV 98 PDF ONLY'
               G_D  = (C_D/(C_D+Q2))**2
               K_val= N_SLAC*(1-G_D**2)*(Q2+C2_val)/(Q2+C1_val)
               K_sea= N_SLAC*Q2/(Q2+C_sea)
*              ------------------------------------------------------- *
*              NON-CHARM PRODUCTION COMPONENTS                         *
*              ------------------------------------------------------- *
               x_0= x_B*(Q2+B_BY)/(Q2+A_BY*x_B)
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*              PREVIOUS METHOD BASED ON CERN PDFLIB LIBRARY
*              CALL PDF(E_nu,x_0,Q2,
*    #                  Uq_0,Ua_0,Dq_0,Da_0,Sq_0,Sa_0,Cq,Ca,G,A)
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*              CURRENT METHOD BASEN ON LHAPDF PACKAGE
               CALL evolvePDF(x_0,sqrt(Q2),f)
               Uq_0= f(+2); Dq_0= f(+1); Sq_0= f(+3); Cq  = f(+4)
               Ua_0= f(-2); Da_0= f(-1); Sa_0= f(-3); Ca  = f(-4)
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
               Uq_0= K_val*Uq_0
               Ua_0= K_sea*Ua_0
               Dq_0= K_val*Dq_0
               Da_0= K_sea*Da_0
               Sq_0= K_val*Sq_0
               Sa_0= K_sea*Sa_0
               SELECTCASE(n_TT)
                     CASE(   1)
                     SELECTCASE(n_NT)
                           CASE(   1)
*                          \nu + p
                           F2_0= 2*x_B*(Dq_0*c2C+Sq_0*s2C+Ua_0)
                           F3_0= 2    *(Dq_0*c2C+Sq_0*s2C-Ua_0)
                           CASE(  -1)
*                          \overline{\nu} + p
                           F2_0= 2*x_B*(Uq_0*c2C+Da_0+Sa_0)
                           F3_0= 2    *(Uq_0*c2C-Da_0-Sa_0)
                  endSELECT
                     CASE(   2)
                     SELECTCASE(n_NT)
                           CASE(   1)
*                          \nu + n
                           F2_0= 2*x_B*(Uq_0*c2C+Sq_0*s2C+Da_0)
                           F3_0= 2    *(Uq_0*c2C+Sq_0*s2C-Da_0)
                           CASE(  -1)
*                          \overline{\nu} + n
                           F2_0= 2*x_B*(Dq_0*c2C+Ua_0+Sa_0)
                           F3_0= 2    *(Dq_0*c2C-Ua_0-Sa_0)
                  endSELECT
            endSELECT
               R_BY=R_WBA(x_0,Q2,1,1)
               F1_0= F2_0/(2*x_B)*(1+4*mm_ini*x_0**2/Q2)/(1+R_BY)
               F4_0= zero
               F5_0= zero
*              ------------------------------------------------------- *
*              CHARM PRODUCTION COMPONENTS                             *
*              ------------------------------------------------------- *
               x_c=x_B*(Q2+B_BY+mm_cBY)/
     #             (half*Q2*(one+sqrt(one+4*mm_ini*x_B**2/Q2))+A_BY*x_B)
               IF (x_c.ge.one) THEN
                 F1_c= zero
                 F2_c= zero
                 F3_c= zero
                 F4_c= zero
                 F5_c= zero
                               ELSE
*                - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*                PREVIOUS METHOD BASED ON CERN PDFLIB LIBRARY
*                CALL PDF(E_nu,x_c,Q2,
*    #                    Uq,Ua,Dq_c,Da_c,Sq_c,Sa_c,Cq,Ca,G,A)
*                - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*                CURRENT METHOD BASEN ON LHAPDF PACKAGE
                 CALL evolvePDF(x_c,sqrt(Q2),f)
                 Uq= f(+2); Dq_c= f(+1); Sq_c= f(+3); Cq  = f(+4)
                 Ua= f(-2); Da_c= f(-1); Sa_c= f(-3); Ca  = f(-4)
*                - - - - - - - - - - - - - - - - - - - - - - - - - - - *
                 Dq_c= K_val*Dq_c
                 Da_c= K_sea*Da_c
                 Sq_c= K_val*Sq_c
                 Sa_c= K_sea*Sa_c
                 SELECTCASE(n_TT)
                       CASE(   1)
                       SELECTCASE(n_NT)
                             CASE(   1)
*                            \nu + p
                             F2_c= 2*x_B*(Dq_c*s2C+Sq_c*c2C)
                             F3_c= 2*    (Dq_c*s2C+Sq_c*c2C)
                             CASE(  -1)
*                            \overline{\nu} + p
                             F2_c= 2*x_B*(Uq_0*s2C+
     #                                   (Da_c-Da_0+Sa_c-Sa_0)*s2C)
                             F3_c= 2*    (Uq_0*s2C-
     #                                   (Da_c-Da_0+Sa_c-Sa_0)*s2C)
                    endSELECT
                       CASE(   2)
                       SELECTCASE(n_NT)
                             CASE(   1)
*                            \nu + n
                             F2_c= 2*x_B*(Uq_0*s2C+Sq_c*c2C+(Da_c-Da_0))
                             F3_c= 2*    (Uq_0*s2C+Sq_c*c2C-(Da_c-Da_0))
                             CASE(  -1)
*                            \overline{\nu} + n
                             F2_c= 2*x_B*(Dq_c*s2C+(Sa_c-Sa_0))
                             F3_c= 2*    (Dq_c*s2C-(Sa_c-Sa_0))
                    endSELECT
              endSELECT
                 R_BY= R_WBA(x_c,Q2,1,1)
                 F1_c= F2_c/(2*x_B)*(1+4*mm_ini*x_c**2/Q2)/(1+R_BY)
                 F4_c= zero
                 F5_c= zero
            endIF
*              ------------------------------------------------------- *
*              ======================================================= *
               CASE(       3)
*              V.A. Naumov, "1-2" scheme, Ref. [4]
*              ======================================================= *
*              ------------------------------------------------------- *
*              NON-CHARM PRODUCTION COMPONENTS                         *
*              ------------------------------------------------------- *
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*              PREVIOUS METHOD BASED ON CERN PDFLIB LIBRARY
*              CALL PDF(E_nu,x_0,Q2,
*    #                  Uq_0,Ua_0,Dq_0,Da_0,Sq_0,Sa_0,Cq_0,Ca_0,G,A)
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*              CURRENT METHOD BASEN ON LHAPDF PACKAGE
               CALL evolvePDF(x_0,sqrt(Q2),f)
               Uq_0= f(+2); Dq_0= f(+1); Sq_0= f(+3); Cq_0= f(+4)
               Ua_0= f(-2); Da_0= f(-1); Sa_0= f(-3); Ca_0= f(-4)
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
               SELECTCASE(n_TT)
                     CASE(   1)
                     SELECTCASE(n_NT)
                           CASE(   1)
*                          \nu + p
                           F1_0=    Dq_0*c2C+Sq_0*s2C+Ua_0+Ca_0
                           F3_0= 2*(Dq_0*c2C+Sq_0*s2C-Ua_0-Ca_0)
                           CASE(  -1)
*                          \overline{\nu} + p
                           F1_0=    Uq_0*c2C+Cq_0*s2C+Da_0+Sa_0
                           F3_0= 2*(Uq_0*c2C+Cq_0*s2C-Da_0-Sa_0)
                  endSELECT
                     CASE(   2)
                     SELECTCASE(n_NT)
                           CASE(   1)
*                          \nu + n
                           F1_0=    Uq_0*c2C+Sq_0*s2C+Da_0+Ca_0
                           F3_0= 2*(Uq_0*c2C+Sq_0*s2C-Da_0-Ca_0)
                           CASE(  -1)
*                          \overline{\nu} + n
                           F1_0=    Dq_0*c2C+Cq_0*s2C+Ua_0+Sa_0
                           F3_0= 2*(Dq_0*c2C+Cq_0*s2C-Ua_0-Sa_0)
                  endSELECT
            endSELECT
               F2_0=  F1_0*(2*x_B)*
     #               (1+R0(E_nu,x_0,Q2))/(1+4*mm_ini*x_B**2/Q2)
               F4_0= (F2_0/(2*x_B)-F1_0)/(2*x_B)
               F5_0=  F2_0/x_B
*              ------------------------------------------------------- *
*              CHARM PRODUCTION COMPONENTS                             *
*              ------------------------------------------------------- *
               IF (x_c.ge.one) THEN
                 F1_c= zero
                 F2_c= zero
                 F3_c= zero
                 F4_c= zero
                 F5_c= zero
                               ELSE
*                - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*                PREVIOUS METHOD BASED ON CERN PDFLIB LIBRARY
*                CALL PDF(E_nu,x_c,Q2,
*    #                    Uq,Ua,Dq_c,Da_c,Sq_c,Sa_c,Cq,Ca,G,A)
*                - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*                CURRENT METHOD BASEN ON LHAPDF PACKAGE
                 CALL evolvePDF(x_c,sqrt(Q2),f)
                 Uq  = f(+2); Dq_c= f(+1); Sq_c= f(+3); Cq  = f(+4)
                 Ua  = f(-2); Da_c= f(-1); Sa_c= f(-3); Ca  = f(-4)
*                - - - - - - - - - - - - - - - - - - - - - - - - - - - *
                 SELECTCASE(n_TT)
                       CASE(   1)
                       SELECTCASE(n_NT)
                             CASE(   1)
*                            \nu + p
                             IF (x_B        .le.
     #                           one/(1+(mm_X_CqSq_nu_p-mm_p)/Q2).and.
     #                           2*m_p*E_nu .ge.
     #                           (m_lep+m_X_CqSq_nu_p)**2-mm_p)
     #                                                             THEN
                               F1_c=    Dq_c*s2C+Sq_c*c2C
                               F3_c= 2*(Dq_c*s2C+Sq_c*c2C)
                         ELSEIF (x_B        .le.
     #                           one/(1+(mm_X_CqDq_nu_p-mm_p)/Q2).and.
     #                           2*m_p*E_nu .ge.
     #                           (m_lep+m_X_CqDq_nu_p)**2-mm_p)
     #                                                             THEN
                               F1_c=   Dq_c*s2C
                               F3_c= 2*Dq_c*s2C
                                                                   ELSE
                               F1_c= zero
                               F3_c= zero
                          endIF
                             CASE(  -1)
*                            \overline{\nu} + p
                             IF (x_B        .le.
     #                           one/(1+(mm_X_CqSa_an_p-mm_p)/Q2).and.
     #                           2*m_p*E_nu .ge.
     #                           (m_lep+m_X_CqSa_an_p)**2-mm_p)
     #                                                             THEN
                               F1_c= Uq_0*s2C+Cq_0*c2C+(Da_c-Da_0)*s2C+
     #                                                 (Sa_c-Sa_0)*c2C
                               F3_c= 2*
     #                               (Uq_0*s2C+Cq_0*c2C-(Da_c-Da_0)*s2C-
     #                                                  (Sa_c-Sa_0)*c2C)
                         ELSEIF (x_B        .le.
     #                           one/(1+(mm_X_CqDa_an_p-mm_p)/Q2).and.
     #                           2*m_p*E_nu .ge.
     #                           (m_lep+m_X_CqDa_an_p)**2-mm_p)
     #                                                             THEN
                               F1_c=  Uq_0*s2C+Cq_0*c2C+(Da_c-Da_0)*s2C
                               F3_c= 2*
     #                               (Uq_0*s2C+Cq_0*c2C-(Da_c-Da_0)*s2C)
                                                                   ELSE
                               F1_c= zero
                               F3_c= zero
                          endIF
                    endSELECT
                       CASE(   2)
                       SELECTCASE(n_NT)
                             CASE(   1)
*                            \nu + n
                             IF (x_B        .le.
     #                           one/(1+(mm_X_CqSq_nu_n-mm_n)/Q2).and.
     #                           2*m_n*E_nu .ge.
     #                           (m_lep+m_X_CqSq_nu_n)**2-mm_n)
     #                                                             THEN
                               F1_c=    Uq_0*s2C+Sq_c*c2C
                               F3_c= 2*(Uq_0*s2C+Sq_c*c2C)
                                                                   ELSE
                               F1_c= zero
                               F3_c= zero
                          endIF
                             CASE(  -1)
*                            \overline{\nu} + n
                             IF (x_B        .le.
     #                           one/(1+(mm_X_CqSa_an_n-mm_n)/Q2).and.
     #                           2*m_n*E_nu .ge.
     #                           (m_lep+m_X_CqSa_an_n)**2-mm_n)
     #                                                             THEN
                               F1_c=  Dq_0*s2C+Cq_0*c2C+(Sa_c-Sa_0)*c2C
                               F3_c= 2*
     #                               (Dq_0*s2C+Cq_0*c2C-(Sa_c-Sa_0)*c2C)
                                                                   ELSE
                               F1_c= zero
                               F3_c= zero
                          endIF
                    endSELECT
              endSELECT
                 SELECTCASE(n_Rc_DIS)
                       CASE(       0)
                       R= R0(E_nu,x_0,    Q2)
                       CASE(       1)
                       R= Rc(E_nu,x_0,x_c,Q2)
              endSELECT
                 F2_c= F1_c*(2*x_B)*(1+R)/(1+4*mm_ini*x_B**2/Q2)
                 F4_c= zero
                 F5_c= zero
            endIF
*              ------------------------------------------------------- *
*              ======================================================= *
               CASE(       4)
*              Yang, Ref. [5]
*              ======================================================= *
               x_0= x_B
               x_c= x_0*(1+mm_c/Q2)
*              ------------------------------------------------------- *
*              NON-CHARM PRODUCTION COMPONENTS                         *
*              ------------------------------------------------------- *
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*              PREVIOUS METHOD BASED ON CERN PDFLIB LIBRARY
*              CALL PDF(E_nu,x_0,Q2,
*    #                  Uq_0,Ua_0,Dq_0,Da_0,Sq_0,Sa_0,Cq_0,Ca_0,G,A)
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*              CURRENT METHOD BASEN ON LHAPDF PACKAGE
               CALL evolvePDF(x_0,sqrt(Q2),f)
               Uq_0= f(+2); Dq_0= f(+1); Sq_0= f(+3); Cq_0= f(+4)
               Ua_0= f(-2); Da_0= f(-1); Sa_0= f(-3); Ca_0= f(-4)
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
               SELECTCASE(n_TT)
                     CASE(   1)
                     SELECTCASE(n_NT)
                           CASE(   1)
*                          \nu + p
                           F1_0=    Dq_0*c2C+Sq_0*s2C+Ua_0+Ca_0
                           F3_0= 2*(Dq_0*c2C+Sq_0*s2C-Ua_0-Ca_0)
                           CASE(  -1)
*                          \overline{\nu} + p
                           F1_0=    Uq_0*c2C+Cq_0*s2C+Da_0+Sa_0
                           F3_0= 2*(Uq_0*c2C+Cq_0*s2C-Da_0-Sa_0)
                  endSELECT
                     CASE(   2)
                     SELECTCASE(n_NT)
                           CASE(   1)
*                          \nu + n
                           F1_0=    Uq_0*c2C+Sq_0*s2C+Da_0+Ca_0
                           F3_0= 2*(Uq_0*c2C+Sq_0*s2C-Da_0-Ca_0)
                           CASE(  -1)
*                          \overline{\nu} + n
                           F1_0=    Dq_0*c2C+Cq_0*s2C+Ua_0+Sa_0
                           F3_0= 2*(Dq_0*c2C+Cq_0*s2C-Ua_0-Sa_0)
                  endSELECT
            endSELECT
               F2_0=  F1_0*(2*x_0)*
     #               (1+R0(E_nu,x_0,Q2))/(1+4*mm_ini*x_0**2/Q2)
               F4_0= (F2_0/(2*x_0)-F1_0)/(2*x_0)
               F5_0=  F2_0/x_0
*              ------------------------------------------------------- *
*              CHARM PRODUCTION COMPONENTS                             *
*              ------------------------------------------------------- *
               IF (x_c.ge.one) THEN
                 F1_c= zero
                 F2_c= zero
                 F3_c= zero
                 F4_c= zero
                 F5_c= zero
                               ELSE
*                - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*                PREVIOUS METHOD BASED ON CERN PDFLIB LIBRARY
*                CALL PDF(E_nu,x_c,Q2,
*    #                    Uq,Ua,Dq_c,Da_c,Sq_c,Sa_c,Cq_0,Ca,G,A)
*                - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*                CURRENT METHOD BASEN ON LHAPDF PACKAGE
                 CALL evolvePDF(x_c,sqrt(Q2),f)
                 Uq  = f(+2); Dq_c= f(+1); Sq_c= f(+3); Cq  = f(+4)
                 Ua  = f(-2); Da_c= f(-1); Sa_c= f(-3); Ca  = f(-4)
*                - - - - - - - - - - - - - - - - - - - - - - - - - - - *
                 SELECTCASE(n_TT)
                       CASE(   1)
                       SELECTCASE(n_NT)
                             CASE(   1)
*                            \nu + p
                             IF (x_B       .le.
     #                           one/(1+(mm_X_CqSq_nu_p-mm_p)/Q2).and.
     #                           2*m_p*E_nu.ge.
     #                           (m_lep+m_X_CqSq_nu_p)**2-mm_p)
     #                                                             THEN
                               F1_c=    Dq_c*s2C+Sq_c*c2C
                               F3_c= 2*(Dq_c*s2C+Sq_c*c2C)
                         ELSEIF (x_B       .le.
     #                           one/(1+(mm_X_CqDq_nu_p-mm_p)/Q2).and.
     #                           2*m_p*E_nu.ge.
     #                           (m_lep+m_X_CqDq_nu_p)**2-mm_p)
     #                                                             THEN
                               F1_c=   Dq_c*s2C
                               F3_c= 2*Dq_c*s2C
                                                                   ELSE
                               F1_c= zero
                               F3_c= zero
                          endIF
                             CASE(  -1)
*                            \overline{\nu} + p
                             IF (x_B       .le.
     #                           one/(1+(mm_X_CqSa_an_p-mm_p)/Q2).and.
     #                           2*m_p*E_nu.ge.
     #                           (m_lep+m_X_CqSa_an_p)**2-mm_p)
     #                                                             THEN
                               F1_c= Uq_0*s2C+Cq_0*c2C+(Da_c-Da_0)*s2C+
     #                                                 (Sa_c-Sa_0)*c2C
                               F3_c= 2*
     #                               (Uq_0*s2C+Cq_0*c2C-(Da_c-Da_0)*s2C-
     #                                                  (Sa_c-Sa_0)*c2C)
                         ELSEIF (x_B       .le.
     #                           one/(1+(mm_X_CqDa_an_p-mm_p)/Q2).and.
     #                           2*m_p*E_nu.ge.
     #                           (m_lep+m_X_CqDa_an_p)**2-mm_p)
     #                                                             THEN
                               F1_c= Uq_0*s2C+Cq_0*c2C+(Da_c-Da_0)*s2C
                               F3_c= 2*
     #                               (Uq_0*s2C+Cq_0*c2C-(Da_c-Da_0)*s2C)
                                                                   ELSE
                               F1_c= zero
                               F3_c= zero
                          endIF
                    endSELECT
                       CASE(   2)
                       SELECTCASE(n_NT)
                             CASE(   1)
*                            \nu + n
                             IF (x_B       .le.
     #                           one/(1+(mm_X_CqSq_nu_n-mm_n)/Q2).and.
     #                           2*m_n*E_nu.ge.
     #                           (m_lep+m_X_CqSq_nu_n)**2-mm_n)
     #                                                             THEN
                               F1_c=    Uq_0*s2C+Sq_c*c2C
                               F3_c= 2*(Uq_0*s2C+Sq_c*c2C)
                                                                   ELSE
                               F1_c= zero
                               F3_c= zero
                          endIF
                             CASE(  -1)
*                            \overline{\nu} + n
                             IF (x_B       .le.
     #                           one/(1+(mm_X_CqSa_an_n-mm_n)/Q2).and.
     #                           2*m_n*E_nu.ge.
     #                           (m_lep+m_X_CqSa_an_n)**2-mm_n)
     #                                                             THEN
                               F1_c= Dq_0*s2C+Cq_0*c2C+(Sa_c-Sa_0)*c2C
                               F3_c= 2*
     #                               (Dq_0*s2C+Cq_0*c2C-(Sa_c-Sa_0)*c2C)
                                                                   ELSE
                               F1_c= zero
                               F3_c= zero
                          endIF
                    endSELECT
              endSELECT
                 SELECTCASE(n_Rc_DIS)
                       CASE(       0)
                       R= R0(E_nu,x_0,    Q2)
                       CASE(       1)
                       R= Rc(E_nu,x_0,x_c,Q2)
              endSELECT
                 F2_c= F1_c*(2*x_c)*(1+R)/(1+4*mm_ini*x_c**2/Q2)
                 F4_c= zero
                 F5_c= zero
            endIF
*              ------------------------------------------------------- *
*              ======================================================= *
               CASE(       5)
*              V.A. Naumov, "QCD" scheme, Ref. [4]
*              ======================================================= *
*              ------------------------------------------------------- *
*              NON-CHARM PRODUCTION COMPONENTS                         *
*              ------------------------------------------------------- *
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*              PREVIOUS METHOD BASED ON CERN PDFLIB LIBRARY
*              CALL PDF(E_nu,x_0,Q2,
*    #                  Uq_0,Ua_0,Dq_0,Da_0,Sq_0,Sa_0,Cq_0,Ca_0,G,A)
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*              CURRENT METHOD BASEN ON LHAPDF PACKAGE
               CALL evolvePDF(x_0,sqrt(Q2),f)
               Uq_0= f(+2); Dq_0= f(+1); Sq_0= f(+3); Cq_0= f(+4)
               Ua_0= f(-2); Da_0= f(-1); Sa_0= f(-3); Ca_0= f(-4)
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
               SELECTCASE(n_TT)
                     CASE(   1)
                     SELECTCASE(n_NT)
                           CASE(   1)
*                          \nu + p
                           F2_0= 2*x_B*(Dq_0*c2C+Sq_0*s2C+Ua_0+Ca_0)
                           F3_0= 2    *(Dq_0*c2C+Sq_0*s2C-Ua_0-Ca_0)
                           CASE(  -1)
*                          \overline{\nu} + p
                           F2_0= 2*x_B*(Uq_0*c2C+Cq_0*s2C+Da_0+Sa_0)
                           F3_0= 2    *(Uq_0*c2C+Cq_0*s2C-Da_0-Sa_0)
                  endSELECT
                     CASE(   2)
                     SELECTCASE(n_NT)
                           CASE(   1)
*                          \nu + n
                           F2_0= 2*x_B*(Uq_0*c2C+Sq_0*s2C+Da_0+Ca_0)
                           F3_0= 2    *(Uq_0*c2C+Sq_0*s2C-Da_0-Ca_0)
                           CASE(  -1)
*                          \overline{\nu} + n
                           F2_0= 2*x_B*(Dq_0*c2C+Cq_0*s2C+Ua_0+Sa_0)
                           F3_0= 2    *(Dq_0*c2C+Cq_0*s2C-Ua_0-Sa_0)
                  endSELECT
            endSELECT
               F1_0=(F2_0*(1+4*mm_ini*x_B**2/Q2)-FQCD_L(x_0,Q2))/(2*x_B)
               F2_0= F1_0*(2*x_B)*(1+R_Liang(x_0,Q2))/
     #                            (1+4*mm_ini*x_B**2/Q2)
               F4_0=(F2_0/(2*x_B)-F1_0)/(2*x_B)
               F5_0= F2_0/x_B
*              ------------------------------------------------------- *
*              CHARM PRODUCTION COMPONENTS                             *
*              ------------------------------------------------------- *
               IF (x_c.ge.one) THEN
                 F1_c= zero
                 F2_c= zero
                 F3_c= zero
                 F4_c= zero
                 F5_c= zero
                               ELSE
*                - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*                PREVIOUS METHOD BASED ON CERN PDFLIB LIBRARY
*                CALL PDF(E_nu,x_c,Q2,
*    #                    Uq,Ua,Dq_c,Da_c,Sq_c,Sa_c,Cq,Ca,G,A)
*                - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*                CURRENT METHOD BASEN ON LHAPDF PACKAGE
                 CALL evolvePDF(x_c,sqrt(Q2),f)
                 Uq  = f(+2); Dq_c= f(+1); Sq_c= f(+3); Cq  = f(+4)
                 Ua  = f(-2); Da_c= f(-1); Sa_c= f(-3); Ca  = f(-4)
*                - - - - - - - - - - - - - - - - - - - - - - - - - - - *
                 SELECTCASE(n_TT)
                       CASE(   1)
                       SELECTCASE(n_NT)
                             CASE(   1)
*                            \nu + p
                             IF (x_B       .le.
     #                           one/(1+(mm_X_CqSq_nu_p-mm_p)/Q2).and.
     #                           2*m_p*E_nu.ge.
     #                           (m_lep+m_X_CqSq_nu_p)**2-mm_p)
     #                                                             THEN
                               F2_c= 2*x_B*(Dq_c*s2C+Sq_c*c2C)
                               F3_c= 2*    (Dq_c*s2C+Sq_c*c2C)
                         ELSEIF (x_B       .le.
     #                           one/(1+(mm_X_CqDq_nu_p-mm_p)/Q2).and.
     #                           2*m_p*E_nu.ge.
     #                           (m_lep+m_X_CqDq_nu_p)**2-mm_p)
     #                                                             THEN
                               F2_c= 2*x_B*(Dq_c*s2C)
                               F3_c= 2*    (Dq_c*s2C)
                                                                   ELSE
                               F2_c= zero
                               F3_c= zero
                          endIF
                             CASE(  -1)
*                            \overline{\nu} + p
                             IF (x_B       .le.
     #                           one/(1+(mm_X_CqSa_an_p-mm_p)/Q2).and.
     #                           2*m_p*E_nu.ge.
     #                           (m_lep+m_X_CqSa_an_p)**2-mm_p)
     #                                                             THEN
                               F2_c= 2*x_B*
     #                               (Uq_0*s2C+Cq_0*c2C+(Da_c-Da_0)*s2C+
     #                                                  (Sa_c-Sa_0)*c2C)
                               F3_c= 2*
     #                               (Uq_0*s2C+Cq_0*c2C-(Da_c-Da_0)*s2C-
     #                                                  (Sa_c-Sa_0)*c2C)
                         ELSEIF (x_B       .le.
     #                           one/(1+(mm_X_CqDa_an_p-mm_p)/Q2).and.
     #                           2*m_p*E_nu.ge.
     #                           (m_lep+m_X_CqDa_an_p)**2-mm_p)
     #                                                             THEN
                               F2_c= 2*x_B*
     #                               (Uq_0*s2C+Cq_0*c2C+(Da_c-Da_0)*s2C)
                               F3_c= 2*
     #                               (Uq_0*s2C+Cq_0*c2C-(Da_c-Da_0)*s2C)
                                                                   ELSE
                               F2_c= zero
                               F3_c= zero
                          endIF
                    endSELECT
                       CASE(   2)
                       SELECTCASE(n_NT)
                             CASE(   1)
*                            \nu + n
                             IF (x_B       .le.
     #                           one/(1+(mm_X_CqSq_nu_n-mm_n)/Q2).and.
     #                           2*m_n*E_nu.ge.
     #                           (m_lep+m_X_CqSq_nu_n)**2-mm_n)
     #                                                             THEN
                               F2_c= 2*x_B*(Uq_0*s2C+Sq_c*c2C)
                               F3_c= 2*    (Uq_0*s2C+Sq_c*c2C)
                                                                   ELSE
                               F2_c= zero
                               F3_c= zero
                          endIF
                             CASE(  -1)
*                            \overline{\nu} + n
                             IF (x_B       .le.
     #                           one/(1+(mm_X_CqSa_an_n-mm_n)/Q2).and.
     #                           2*m_n*E_nu.ge.
     #                           (m_lep+m_X_CqSa_an_n)**2-mm_n)
     #                                                             THEN
                               F2_c= 2*x_B*
     #                               (Dq_0*s2C+Cq_0*c2C+(Sa_c-Sa_0)*c2C)
                               F3_c= 2*
     #                               (Dq_0*s2C+Cq_0*c2C-(Sa_c-Sa_0)*c2C)
                                                                   ELSE
                               F2_c= zero
                               F3_c= zero
                          endIF
                    endSELECT
              endSELECT
                 F1_c= (F2_c*(1+4*mm_ini*x_B**2/Q2)-FQCD_L(x_c,Q2))/
     #                 (2*x_B)
                 F2_c= F1_c*(2*x_B)*(1+R_Liang(x_c,Q2))/
     #                              (1+4*mm_ini*x_B**2/Q2)
                 F4_c= zero
                 F5_c= zero
            endIF
*              ------------------------------------------------------- *
*              ======================================================= *
               CASE(       6)
*              V.A. Naumov, a test scheme, Ref. [4]
*              ======================================================= *
*              ------------------------------------------------------- *
*              NON-CHARM PRODUCTION COMPONENTS                         *
*              ------------------------------------------------------- *
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*              PREVIOUS METHOD BASED ON CERN PDFLIB LIBRARY
*              CALL PDF(E_nu,x_0,Q2,
*    #                  Uq_0,Ua_0,Dq_0,Da_0,Sq_0,Sa_0,Cq_0,Ca_0,G,A)
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*              CURRENT METHOD BASEN ON LHAPDF PACKAGE
               CALL evolvePDF(x_0,sqrt(Q2),f)
               Uq_0= f(+2); Dq_0= f(+1); Sq_0= f(+3); Cq_0= f(+4)
               Ua_0= f(-2); Da_0= f(-1); Sa_0= f(-3); Ca_0= f(-4)
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
               SELECTCASE(n_TT)
                     CASE(   1)
                     SELECTCASE(n_NT)
                           CASE(   1)
*                          \nu + p
                           F2_0= 2*x_B*(Dq_0*c2C+Sq_0*s2C+Ua_0+Ca_0)
                           F3_0= 2    *(Dq_0*c2C+Sq_0*s2C-Ua_0-Ca_0)
                           CASE(  -1)
*                          \overline{\nu} + p
                           F2_0= 2*x_B*(Uq_0*c2C+Cq_0*s2C+Da_0+Sa_0)
                           F3_0= 2    *(Uq_0*c2C+Cq_0*s2C-Da_0-Sa_0)
                  endSELECT
                     CASE(   2)
                     SELECTCASE(n_NT)
                           CASE(   1)
*                          \nu + n
                           F2_0= 2*x_B*(Uq_0*c2C+Sq_0*s2C+Da_0+Ca_0)
                           F3_0= 2    *(Uq_0*c2C+Sq_0*s2C-Da_0-Ca_0)
                           CASE(  -1)
*                          \overline{\nu} + n
                           F2_0= 2*x_B*(Dq_0*c2C+Cq_0*s2C+Ua_0+Sa_0)
                           F3_0= 2    *(Dq_0*c2C+Cq_0*s2C-Ua_0-Sa_0)
                  endSELECT
            endSELECT
               A   = (one+4*mm_ini*x_B**2/Q2)/(one+R0(E_nu,x_0,Q2))
               F1_0= half*(one+    A)*F2_0/(2*x_B)
               F2_0= half*(one+one/A)*F2_0
               F4_0= (F2_0/(2*x_B)-F1_0)/(2*x_B)
               F5_0=  F2_0/x_B
*              ------------------------------------------------------- *
*              CHARM PRODUCTION COMPONENTS                             *
*              ------------------------------------------------------- *
               IF (x_c.ge.one) THEN
                 F1_c= zero
                 F2_c= zero
                 F3_c= zero
                 F4_c= zero
                 F5_c= zero
                               ELSE
*                - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*                PREVIOUS METHOD BASED ON CERN PDFLIB LIBRARY
*                CALL PDF(E_nu,x_c,Q2,
*    #                    Uq,Ua,Dq_c,Da_c,Sq_c,Sa_c,Cq,Ca,G,A)
*                - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*                CURRENT METHOD BASEN ON LHAPDF PACKAGE
                 CALL evolvePDF(x_c,sqrt(Q2),f)
                 Uq  = f(+2); Dq_c= f(+1); Sq_c= f(+3); Cq  = f(+4)
                 Ua  = f(-2); Da_c= f(-1); Sa_c= f(-3); Ca  = f(-4)
*                - - - - - - - - - - - - - - - - - - - - - - - - - - - *
                 SELECTCASE(n_TT)
                       CASE(   1)
                       SELECTCASE(n_NT)
                             CASE(   1)
*                            \nu + p
                             IF (x_B       .le.
     #                           one/(1+(mm_X_CqSq_nu_p-mm_p)/Q2).and.
     #                           2*m_p*E_nu.ge.
     #                           (m_lep+m_X_CqSq_nu_p)**2-mm_p)
     #                                                             THEN
                               F2_c= 2*x_B*(Dq_c*s2C+Sq_c*c2C)
                               F3_c= 2*    (Dq_c*s2C+Sq_c*c2C)
                         ELSEIF (x_B       .le.
     #                           one/(1+(mm_X_CqDq_nu_p-mm_p)/Q2).and.
     #                           2*m_p*E_nu.ge.
     #                           (m_lep+m_X_CqDq_nu_p)**2-mm_p)
     #                                                             THEN
                               F2_c= 2*x_B*(Dq_c*s2C)
                               F3_c= 2*    (Dq_c*s2C)
                                                                   ELSE
                               F2_c= zero
                               F3_c= zero
                          endIF
                             CASE(  -1)
*                            \overline{\nu} + p
                             IF (x_B       .le.
     #                           one/(1+(mm_X_CqSa_an_p-mm_p)/Q2).and.
     #                           2*m_p*E_nu.ge.
     #                           (m_lep+m_X_CqSa_an_p)**2-mm_p)
     #                                                             THEN
                               F2_c= 2*x_B*
     #                               (Uq_0*s2C+Cq_0*c2C+(Da_c-Da_0)*s2C+
     #                                                  (Sa_c-Sa_0)*c2C)
                               F3_c= 2*
     #                               (Uq_0*s2C+Cq_0*c2C-(Da_c-Da_0)*s2C-
     #                                                  (Sa_c-Sa_0)*c2C)
                         ELSEIF (x_B       .le.
     #                           one/(1+(mm_X_CqDa_an_p-mm_p)/Q2).and.
     #                           2*m_p*E_nu.ge.
     #                           (m_lep+m_X_CqDa_an_p)**2-mm_p)
     #                                                             THEN
                               F2_c= 2*x_B*
     #                               (Uq_0*s2C+Cq_0*c2C+(Da_c-Da_0)*s2C)
                               F3_c= 2*
     #                               (Uq_0*s2C+Cq_0*c2C-(Da_c-Da_0)*s2C)
                                                                   ELSE
                               F2_c= zero
                               F3_c= zero
                          endIF
                    endSELECT
                       CASE(   2)
                       SELECTCASE(n_NT)
                             CASE(   1)
*                            \nu + n
                             IF (x_B       .le.
     #                           one/(1+(mm_X_CqSq_nu_n-mm_n)/Q2).and.
     #                           2*m_n*E_nu.ge.
     #                           (m_lep+m_X_CqSq_nu_n)**2-mm_n)
     #                                                             THEN
                               F2_c= 2*x_B*(Uq_0*s2C+Sq_c*c2C)
                               F3_c= 2*    (Uq_0*s2C+Sq_c*c2C)
                                                                   ELSE
                               F2_c= zero
                               F3_c= zero
                          endIF
                             CASE(  -1)
*                            \overline{\nu} + n
                             IF (x_B       .le.
     #                           one/(1+(mm_X_CqSa_an_n-mm_n)/Q2).and.
     #                           2*m_n*E_nu.ge.
     #                           (m_lep+m_X_CqSa_an_n)**2-mm_n)
     #                                                             THEN
                               F2_c= 2*x_B*
     #                               (Dq_0*s2C+Cq_0*c2C+(Sa_c-Sa_0)*c2C)
                               F3_c= 2*
     #                               (Dq_0*s2C+Cq_0*c2C-(Sa_c-Sa_0)*c2C)
                                                                   ELSE
                               F2_c= zero
                               F3_c= zero
                          endIF
                    endSELECT
              endSELECT
                 SELECTCASE(n_Rc_DIS)
                       CASE(       0)
                       FL_c= F0_L(E_nu,x_0,    Q2,F2_c)
                       CASE(       1)
                       FL_c= Fc_L(E_nu,x_0,x_c,Q2,F2_c)
              endSELECT
                 SELECTCASE(n_Rc_DIS)
                       CASE(       0)
                       R= R0(E_nu,x_0,    Q2)
                       CASE(       1)
                       R= Rc(E_nu,x_0,x_c,Q2)
              endSELECT
                 A   = (one+4*mm_ini*x_B**2/Q2)/(one+R)
                 F1_c= half*(one+    A)*F2_c/(2*x_B)
                 F2_c= half*(one+one/A)*F2_c
                 F4_c= zero
                 F5_c= zero
            endIF
*              ------------------------------------------------------- *
*              ======================================================= *
      endSELECT
         F1= F1_0+F1_c
         F2= F2_0+F2_c
         F3= F3_0+F3_c
         F4= F4_0+F4_c
         F5= F5_0+F5_c
         F6= zero

         RETURN

*     ==================================================================
      ENTRY SFNC(E_nu,x_B,Q2,F1,F2,F3)
*     ==================================================================
         SELECTCASE(n_AG_DIS)
*              ======================================================= *
               CASE(       0)
*              E.A. Paschos and J.Y. Yu, Ref. [1]
*              ======================================================= *
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*              PREVIOUS METHOD BASED ON CERN PDFLIB LIBRARY
*              CALL PDF(E_nu,x_B,Q2,
*    #                  Uq_0,Ua_0,Dq_0,Da_0,Sq_0,Sa_0,Cq_0,Ca_0,G,A)
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*              CURRENT METHOD BASEN ON LHAPDF PACKAGE
               CALL evolvePDF(x_B,sqrt(Q2),f)
               Uq_0= f(+2); Dq_0= f(+1); Sq_0= f(+3); Cq_0= f(+4)
               Ua_0= f(-2); Da_0= f(-1); Sa_0= f(-3); Ca_0= f(-4)
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
               SELECTCASE(n_TT)
                     CASE(   1)
*                    \nu(\overline{\nu}) + p
                     F2_0= 2*x_B*(g2_0LRp*(Uq_0+Cq_0+Ua_0+Ca_0)+
     #                            g2_1LRp*(Dq_0+Sq_0+Da_0+Sa_0))
                     F3_0= 2    *(g2_0LRm*(Uq_0+Cq_0-Ua_0-Ca_0)+
     #                            g2_1LRm*(Dq_0+Sq_0-Da_0-Sa_0))
                     CASE(   2)
*                    \nu(\overline{\nu}) + n
                     F2_0= 2*x_B*(g2_0LRp*(Dq_0+Cq_0+Da_0+Ca_0)+
     #                            g2_1LRp*(Uq_0+Sq_0+Ua_0+Sa_0))
                     F3_0= 2    *(g2_0LRm*(Dq_0+Cq_0-Da_0-Ca_0)+
     #                            g2_1LRm*(Uq_0+Sq_0-Ua_0-Sa_0))
            endSELECT
               F1_0= F2_0/(2*x_B)
*              ======================================================= *
               CASE(       1)
*              V.A. Naumov and K.S. Kuzmin, Ref. [2]
*              ======================================================= *
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*              PREVIOUS METHOD BASED ON CERN PDFLIB LIBRARY
*              CALL PDF(E_nu,x_B,Q2,
*    #                   Uq_0,Ua_0,Dq_0,Da_0,Sq_0,Sa_0,Cq_0,Ca_0,G,A)
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*              CURRENT METHOD BASEN ON LHAPDF PACKAGE
               CALL evolvePDF(x_B,sqrt(Q2),f)
               Uq_0= f(+2); Dq_0= f(+1); Sq_0= f(+3); Cq_0= f(+4)
               Ua_0= f(-2); Da_0= f(-1); Sa_0= f(-3); Ca_0= f(-4)
*              - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
               SELECTCASE(n_TT)
                     CASE(   1)
*                    \nu(\overline{\nu}) + p
                     F2_0= 2*x_B*(g2_0LRp*(Uq_0+Cq_0+Ua_0+Ca_0)+
     #                            g2_1LRp*(Dq_0+Sq_0+Da_0+Sa_0))
                     F3_0= 2    *(g2_0LRm*(Uq_0+Cq_0-Ua_0-Ca_0)+
     #                            g2_1LRm*(Dq_0+Sq_0-Da_0-Sa_0))
                     CASE(   2)
*                    \nu(\overline{\nu}) + n
                     F2_0= 2*x_B*(g2_0LRp*(Dq_0+Cq_0+Da_0+Ca_0)+
     #                            g2_1LRp*(Uq_0+Sq_0+Ua_0+Sa_0))
                     F3_0= 2    *(g2_0LRm*(Dq_0+Cq_0-Da_0-Ca_0)+
     #                            g2_1LRm*(Uq_0+Sq_0-Ua_0-Sa_0))
            endSELECT
               F1_0= F2_0/(2*x_B)
*              ======================================================= *
      endSELECT
         F1= F1_0
         F2= F2_0
         F3= F3_0

         RETURN
*     ==================================================================

      END SUBROUTINE INITPDF
*      END SUBROUTINE NucleonStructureFunctions
