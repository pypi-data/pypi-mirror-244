************************************************************************
      FUNCTION R_E143(x,Q2,n_R,n_S)
************************************************************************
*                                                                      *
*     REFERENCES                                                       *
*                                                                      *
*     [1] K. Abe et al. (E143 Collaboration), "Measurements of $R=     *
*         \sigma_L/\sigma_T$ for $0.03 < x < 0.1$ and fit to world     *
*         data," Phys. Lett. B 452 (1999) 194-200.                     *
*                                                                      *
*                      A.I. Alikhanov ITEP, Moscow, Russia 2005/06/17  *
************************************************************************

         USE Routines

         IMPLICIT REAL*8 (A-M,O-Z), INTEGER (N)

         REAL*8,PARAMETER::
     #        W2_JLab=2.5**2,
     #        a1=  0.0485, b1=  0.0481, c1=  0.0577,
     #        a2=  0.5470, b2=  0.6114, c2=  0.4644,
     #        a3=  2.0621, b3=- 0.3509, c3=  1.8288,
     #        a4=- 0.3804, b4=- 0.4611, c4= 12.3708,
     #        a5=  0.5090, b5=  0.7172, c5=-43.1043,
     #        a6=- 0.0285, b6=- 0.0317, c6= 41.7415

         COMMON      /m_ini/m_ini,mm_ini                                 Mass of target nucleon

         SELECTCASE(n_S)
*              ------------------------------------------------------- *
               CASE(  0)                                                 Reference model
*              ------------------------------------------------------- *
               SELECTCASE(n_R)
                     CASE(  1)
                     R_E143= a1*Tf(x,Q2)+
     #                       a2*(one+x*(a4+x*a5))*x**a6/
     #                       (Q2**4+a3**4)**quarter
                     CASE(  2)
                     R_E143= b1*Tf(x,Q2)+
     #                       (b2/Q2+b3/(Q2**2+0.09))*
     #                       (one+x*(b4+x*b5))*x**b6
                     CASE(  3)
                     R_E143= c1*Tf(x,Q2)+
     #                       c2/sqrt(c3**2+(Q2-(c4+x*(c5+x*c6))*x)**2)
                     CASE(  4)
                     Ra    = a1*Tf(x,Q2)+
     #                       a2*(one+x*(a4+x*a5))*x**a6/
     #                       (Q2**4+a3**4)**quarter
                     Rb    = b1*Tf(x,Q2)+
     #                       (b2/Q2+b3/(Q2**2+0.09))*
     #                       (one+x*(b4+x*b5))*x**b6
                     Rc    = c1*Tf(x,Q2)+
     #                       c2/sqrt(c3**2+(Q2-(c4+x*(c5+x*c6))*x)**2)
                     R_E143= (Ra+Rb+Rc)*third
            endSELECT
*              ------------------------------------------------------- *
               CASE(  1)                                                 Reference model and JLab modification
*              ------------------------------------------------------- *
               SELECTCASE(n_R)
                     CASE(  1)
                     R_E143= a1*Tf(x,Q2)+
     #                       a2*(one+x*(a4+x*a5))*x**a6/
     #                       (Q2**4+a3**4)**quarter
                     CASE(  2)
                     R_E143= b1*Tf(x,Q2)+
     #                       (b2/Q2+b3/(Q2**2+0.09))*
     #                       (one+x*(b4+x*b5))*x**b6
                     CASE(  3)
                     R_E143= c1*Tf(x,Q2)+
     #                       c2/sqrt(c3**2+(Q2-(c4+x*(c5+x*c6))*x)**2)
                     CASE(  4)
                     Ra    = a1*Tf(x,Q2)+
     #                       a2*(one+x*(a4+x*a5))*x**a6/
     #                       (Q2**4+a3**4)**quarter
                     Rb    = b1*Tf(x,Q2)+
     #                       (b2/Q2+b3/(Q2**2+0.09))*
     #                       (one+x*(b4+x*b5))*x**b6
                     Rc    = c1*Tf(x,Q2)+
     #                       c2/sqrt(c3**2+(Q2-(c4+x*(c5+x*c6))*x)**2)
                     R_E143= (Ra+Rb+Rc)*third
            endSELECT
               IF (Q2*(one-x)/x+mm_ini.lt.W2_JLab) THEN
                 x_0   = Q2/(Q2-mm_ini+W2_JLab)
                 R_E143= ((one-x)/(one-x_0))**3*R_E143
            endIF
*              ------------------------------------------------------- *
      endSELECT

         RETURN
      END FUNCTION R_E143
