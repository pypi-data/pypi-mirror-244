************************************************************************
      FUNCTION F0_L(E_nu,x_0,Q2,F2)
************************************************************************
*                                                                      *
*                                                                      *
************************************************************************

         USE PhysMathConstants, ONLY: zero,one

         INTEGER n_FL_DIS
            REAL*8 F0_L,FQCD_L,R0,E_nu,x_0,Q2,F2,m_ini,mm_ini

         COMMON   /n_FL_DIS/n_FL_DIS                                     Switch for model of function F_L
         COMMON      /m_ini/m_ini,mm_ini                                 Mass of target nucleon

         SELECTCASE(n_FL_DIS)
               CASE(       0);F0_L= zero
               CASE(       1);F0_L= FQCD_L(x_0,Q2)
               CASE(       2);F0_L= (one+4*mm_ini*x_0**2/Q2)*
     #                              R0(E_nu,x_0,Q2)/
     #                              (one+R0(E_nu,x_0,Q2))*F2
      endSELECT

         RETURN
      END FUNCTION F0_L

************************************************************************
      FUNCTION Fc_L(E_nu,x_0,x_c,Q2,F2)
************************************************************************
*                                                                      *
*                                                                      *
************************************************************************

         USE PhysMathConstants, ONLY: zero,one

         INTEGER n_FL_DIS
            REAL*8 Fc_L,FQCD_L,Rc,E_nu,x_0,x_c,Q2,F2,m_ini,mm_ini

         COMMON   /n_FL_DIS/n_FL_DIS                                     Switch for model of function F_L
         COMMON      /m_ini/m_ini,mm_ini                                 Mass of target nucleon

         SELECTCASE(n_FL_DIS)
               CASE(       0);Fc_L= zero
               CASE(       1);Fc_L= FQCD_L(x_c,Q2)
               CASE(       2);Fc_L= (one+4*mm_ini*x_0**2/Q2)*
     #                              Rc(E_nu,x_0,x_c,Q2)/
     #                              (one+Rc(E_nu,x_0,x_c,Q2))*F2
      endSELECT

         RETURN
      END FUNCTION Fc_L
