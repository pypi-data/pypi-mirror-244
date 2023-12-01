************************************************************************
      FUNCTION R_WBA(x,Q2,n_R,n_S)
************************************************************************
*                                                                      *
*                                                                      *
*     REFERENCES                                                       *
*                                                                      *
*     [1] L.W. Whitlow, S. Rock, A. Bodek, E.M. Riordan,  S. Dasu,     *
*         "A  precise  extraction  of  $R=\sigma_L/\sigma_T$  from     *
*         a global  analysis of  the  SLAC  deep  inelastic  $e-p$     *
*         and $e-d$ scattering  cross sections," Phys. Lett. B 250     *
*         (1990) 193-198.                                              *
*     [2] J. Bartelski,  W. Krolikowski and M. Kurzela, "Deep ine-     *
*         lastic ratio $R=\sigma_L/\sigma_T$ and the possible exi-     *
*         stence of scalar partons in the  nucleon," arXiv: hep-ph     *
*         /9804415.                                                    *
*     [3] S.I. Alekhin, "High-twist contribution to the longitudi-     *
*         nal structure function $F_L$ at high $x$," Eur. Phys. J.     *
*         C 12 (2000) 587-593.                                         *
*                                                                      *
************************************************************************

         USE Routines

         IMPLICIT REAL (A-M,O-Z), INTEGER (N)

         INTEGER n_R,n_S
         REAL*8 R_WBA,x,Q2,x_0,m_ini,mm_ini

         REAL*8,PARAMETER::
     #        Q2_0   = 0.35,
     #        W2_JLab= 2.5**2,
     #        o1     = 0.0635, o2= 0.5747, o3=-0.3534,                   Withlow et al.
     #        k1     = 0.041,  k2= 0.592,  k3=-0.331,                    Bartelski et al.
     #        i1     = 0.100,  i2= 0.46,   i3=-0.14                      Alekhin

         COMMON      /m_ini/m_ini,mm_ini                                 Mass of target nucleon

         SELECTCASE(n_S)
*              ------------------------------------------------------- *
               CASE(  0)                                                 Reference model
*              ------------------------------------------------------- *
               SELECTCASE(n_R)
                     CASE(  1); R_WBA= Rg(x,Q2,o1,o2,o3)                 Withlow et al.
                     CASE(  2); R_WBA= Rg(x,Q2,k1,k2,k3)                 Bartelski et al.
                     CASE(  3); R_WBA= Rg(x,Q2,i1,i2,i3)                 Alekhin
            endSELECT
*              ------------------------------------------------------- *
               CASE(  1)                                                 Reference model and smoothing at Q2 < Q2_0
*              ------------------------------------------------------- *
               SELECTCASE(n_R)
                     CASE(  1)                                           Withlow et al.
                     IF (Q2<Q2_0) THEN; R_WBA= Rf(x,Q2,Q2_0,o1,o2,o3)
                                  ELSE; R_WBA= Rg(x,Q2,     o1,o2,o3)
                  endIF
                     CASE(  2)                                           Bartelski et al.
                     IF (Q2<Q2_0) THEN; R_WBA= Rf(x,Q2,Q2_0,k1,k2,k3)
                                  ELSE; R_WBA= Rg(x,Q2,     k1,k2,k3)
                  endIF
                     CASE(  3)                                           Alekhin
                     IF (Q2<Q2_0) THEN; R_WBA= Rf(x,Q2,Q2_0,i1,i2,i3)
                                  ELSE; R_WBA= Rg(x,Q2,     i1,i2,i3)
                  endIF
            endSELECT
*              ------------------------------------------------------- *
               CASE(  2)                                                 Reference model and JLab modification
*              ------------------------------------------------------- *
               SELECTCASE(n_R)
                     CASE(  1); R_WBA= Rg(x_0,Q2,o1,o2,o3)               Withlow et al.
                     CASE(  2); R_WBA= Rg(x_0,Q2,k1,k2,k3)               Bartelski et al.
                     CASE(  3); R_WBA= Rg(x_0,Q2,i1,i2,i3)               Alekhin
            endSELECT
               IF (Q2*(one-x)/x+mm_ini < W2_JLab) THEN
                 x_0  = Q2/(Q2-mm_ini+W2_JLab)
                 R_WBA= ((one-x)/(one-x_0))**3*R_WBA
            endIF
*              ------------------------------------------------------- *
      endSELECT

         RETURN
      END FUNCTION R_WBA
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
c              R=0.0635*(1+(12*Q2)/((1+Q2)*(1+(8*x)**2)))/
c    #           log(25*Q2)+0.5747/Q2-0.3534/((Q2**2)+0.09)
c              IF (Q2 <= 0.35) THEN
c                R=(3.207*Q2/(1+(Q2**2)))*(c1+c2/(1+(8*x)**2))
c                              ELSE
c                R=0.0635*(1+(12*Q2)/((1+Q2)*(1+(8*x)**2)))/
c    #             log(25*Q2)+0.5747/Q2-0.3534/((Q2**2)+0.09)
c           endIF
c              IF (Q2 <= Q2_1) THEN
c                R=(3.207*Q2/(1+(Q2**2)))*(c1+c2/(1+(8*x)**2))
c          ELSEIF (Q2 <= Q2_2) THEN
c                R_0=(3.207*Q2_0/(1+Q2_0**2))*(c1+(c2/(1+(8*x)**2)))
c                R_1=(3.207*Q2_1/(1+Q2_1**2))*(c1+(c2/(1+(8*x)**2)))
c                R_2=0.0635*(1+12*Q2_2/((1+Q2_2)*(1+(8*x)**2)))/
c    #               log(25*Q2_2)+0.5747/Q2_2-0.3534/(Q2_2**2+0.09)
c                R_3=0.0635*(1+12*Q2_3/((1+Q2_3)*(1+(8*x)**2)))/
c    #               log(25*Q2_3)+0.5747/Q2_3-0.3534/(Q2_3**2+0.09)
c                R  =R_0*((Q2  -Q2_1)*(Q2  -Q2_2)*(Q2  -Q2_3))/
c    #                   ((Q2_0-Q2_1)*(Q2_0-Q2_2)*(Q2_0-Q2_3))+
c    #               R_1*((Q2  -Q2_0)*(Q2  -Q2_2)*(Q2  -Q2_3))/
c    #                   ((Q2_1-Q2_0)*(Q2_1-Q2_2)*(Q2_1-Q2_3))+
c    #               R_2*((Q2  -Q2_0)*(Q2  -Q2_1)*(Q2  -Q2_3))/
c    #                   ((Q2_2-Q2_0)*(Q2_2-Q2_1)*(Q2_2-Q2_3))+
c    #               R_3*((Q2  -Q2_0)*(Q2  -Q2_1)*(Q2  -Q2_2))/
c    #                   ((Q2_3-Q2_0)*(Q2_3-Q2_1)*(Q2_3-Q2_2))
c                              ELSE
c                R=0.0635*(1+(12*Q2)/((1+Q2)*(1+(8*x)**2)))/
c    #             log(25*Q2)+0.5747/Q2-0.3534/((Q2**2)+0.09)
c           endIF
cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc
