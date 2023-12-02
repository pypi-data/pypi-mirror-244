************************************************************************
      FUNCTION R_set(E_nu,x_0,Q2)
************************************************************************
*                                                                      *
*                                                                      *
************************************************************************

         USE PhysMathConstants, ONLY: zero,one

         INTEGER n_RT_DIS
         REAL*8 R_set,R0,Rset_Liang,R_Liang,FQCD_L,R_WBA,R_E143,
     #           x_0,Q2,E_nu,F1,F2,F3,F4,F5,F6

         SAVE

         COMMON   /n_RT_DIS/n_RT_DIS                                     Switch for model of function R

         R_set= Rset_Liang(one,one)
         RETURN

*     ==================================================================
      ENTRY R0(E_nu,x_0,Q2)
*     ==================================================================

         SELECTCASE(n_RT_DIS)
               CASE(       0); R0= zero                                  R= 0
               CASE(       1); CALL SFCC (E_nu,x_0,Q2,F1,F2,F3,F4,F5,F6) Altarelli-Martinelli scheme
                               R0= FQCD_L (x_0,Q2)/F2                    QCD model
               CASE(       2); R0= R_Liang(x_0,Q2)                       Liang + R_a
               CASE(       3); R0= R_WBA  (x_0,Q2,1,0)                   Whitlow et al.
               CASE(       4); R0= R_WBA  (x_0,Q2,1,1)                   Whitlow et al. + smoothing
               CASE(       5); R0= R_WBA  (x_0,Q2,1,2)                   Whitlow et al. + JLab
               CASE(       6); R0= R_WBA  (x_0,Q2,2,0)                   Bartelski et al.
               CASE(       7); R0= R_WBA  (x_0,Q2,2,1)                   Bartelski et al. + smoothing
               CASE(       8); R0= R_WBA  (x_0,Q2,2,2)                   Bartelski et al. + JLab
               CASE(       9); R0= R_WBA  (x_0,Q2,3,0)                   Alekhin
               CASE(      10); R0= R_WBA  (x_0,Q2,3,1)                   Alekhin + smoothing
               CASE(      11); R0= R_WBA  (x_0,Q2,3,2)                   Alekhin + JLab
               CASE(      12); R0= R_E143 (x_0,Q2,1,0)                   R_a E-143
               CASE(      13); R0= R_E143 (x_0,Q2,2,0)                   R_b E-143
               CASE(      14); R0= R_E143 (x_0,Q2,3,0)                   R_c E-143
               CASE(      15); R0= R_E143 (x_0,Q2,4,0)                   R1998 E-143
               CASE(      16); R0= R_E143 (x_0,Q2,1,1)                   R_a + JLab
               CASE(      17); R0= R_E143 (x_0,Q2,2,1)                   R_b + JLab
               CASE(      18); R0= R_E143 (x_0,Q2,3,1)                   R_c + JLab
               CASE(      19); R0= R_E143 (x_0,Q2,4,1)                   R1998 + JLab
      endSELECT
         RETURN

*     ==================================================================

      END FUNCTION R_set

************************************************************************
      FUNCTION Rc(E_nu,x_0,x_c,Q2)
************************************************************************
*                                                                      *
*                                                                      *
************************************************************************

         USE PhysMathConstants, ONLY:zero,one,mm_c

         INTEGER n_RT_DIS
            REAL*8 Rc,FQCD_L,R_Liang,R_WBA,R_E143,
     #           E_nu,x_0,x_c,Q2,m_ini,mm_ini,R,F1,F2,F3,F4,F5,F6

         COMMON   /n_RT_DIS/n_RT_DIS                                     Switch for model of function R
         COMMON      /m_ini/m_ini,mm_ini                                 Mass of target nucleon

         SELECTCASE(n_RT_DIS)
               CASE(       0); R= zero                                   R= 0
               CASE(       1); CALL SFCC(E_nu,x_c,Q2,F1,F2,F3,F4,F5,F6)  Altarelli-Martinelli scheme
                               R= FQCD_L (x_c,Q2)/F2                     QCD model
               CASE(       2); R= R_Liang(x_c,Q2)                        Liang + R_a
               CASE(       3); R= R_WBA  (x_c,Q2,1,0)                    Whitlow et al.
               CASE(       4); R= R_WBA  (x_c,Q2,1,1)                    Whitlow et al.   + smoothing
               CASE(       5); R= R_WBA  (x_c,Q2,1,2)                    Whitlow et al.   + JLab
               CASE(       6); R= R_WBA  (x_c,Q2,2,0)                    Bartelski et al.
               CASE(       7); R= R_WBA  (x_c,Q2,2,1)                    Bartelski et al. + smoothing
               CASE(       8); R= R_WBA  (x_c,Q2,2,2)                    Bartelski et al. + JLab
               CASE(       9); R= R_WBA  (x_c,Q2,3,0)                    Alekhin
               CASE(      10); R= R_WBA  (x_c,Q2,3,1)                    Alekhin          + smoothing
               CASE(      11); R= R_WBA  (x_c,Q2,3,2)                    Alekhin          + JLab
               CASE(      12); R= R_E143 (x_c,Q2,1,0)                    R_a E-143
               CASE(      13); R= R_E143 (x_c,Q2,2,0)                    R_b E-143
               CASE(      14); R= R_E143 (x_c,Q2,3,0)                    R_c E-143
               CASE(      15); R= R_E143 (x_c,Q2,4,0)                    R1998 E-143
               CASE(      16); R= R_E143 (x_c,Q2,1,1)                    R_a E-143        + JLab
               CASE(      17); R= R_E143 (x_c,Q2,2,1)                    R_b E-143        + JLab
               CASE(      18); R= R_E143 (x_c,Q2,3,1)                    R_c E-143        + JLab
               CASE(      19); R= R_E143 (x_c,Q2,4,1)                    R1998 E-143      + JLab
      endSELECT
         Rc= (one+mm_c/Q2)*(one+R)*(one+4*mm_ini*x_0**2/Q2)/
     #                             (one+4*mm_ini*x_c**2/Q2)-one

         RETURN
      END FUNCTION Rc
