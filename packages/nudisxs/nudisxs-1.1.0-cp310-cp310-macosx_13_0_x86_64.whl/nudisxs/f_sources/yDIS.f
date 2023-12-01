************************************************************************
      SUBROUTINE y1DIS_lim(E_nu,x,y_min,y_max)
************************************************************************
*                                                                      *
*                                                                      *
************************************************************************

         USE PhysMathConstants, ONLY: zero,one

         IMPLICIT REAL*8 (A-Z)

         COMMON      /m_ini/m_ini,mm_ini                                 Mass of target nucleon
         COMMON      /m_lep/m_lep,mm_lep                                 Mass of final charged lepton
         COMMON      /m_fin/m_fin,mm_fin                                 Mass of final hadron or hadron system
         COMMON    /y_limit/y_l,y_u,y_c                                  Mass of final hadron or hadron system

         y_min= zero
         y_max= one
         IF (m_ini.eq.m_fin) THEN
           a    = (one-mm_lep*(one+E_nu/(m_ini*x))/(2*E_nu**2))/
     #            (2*(one+m_ini*x/(2*E_nu)))
           b    = sqrt((one-mm_lep/(2*m_ini*x*E_nu))**2-mm_lep/E_nu**2)/
     #            (2*(one+m_ini*x/(2*E_nu)))
           y_min= a-b
           y_max= a+b
                             ELSE
           y_cut= (mm_fin-mm_ini)/(2*m_ini*(one-x)*E_nu)
           y_min= (one-mm_lep*(one+E_nu/(m_ini*x))/(2*E_nu**2)-
     #            sqrt((one-mm_lep/(2*(m_ini*x)*E_nu))**2-
     #            mm_lep/E_nu**2))/(2*(one+(m_ini*x)/(2*E_nu)))
           y_min= max(y_min,y_cut)
           y_max= (one-mm_lep*(one+E_nu/(m_ini*x))/(2*E_nu**2)+
     #            sqrt((one-mm_lep/(2*(m_ini*x)*E_nu))**2-
     #            mm_lep/E_nu**2))/(2*(one+(m_ini*x)/(2*E_nu)))
      endIF
         y_c= y_cut
         IF (y_min<zero .or. y_max<zero) THEN
                y_l= zero
                y_u= zero
                                         ELSE
                y_l= y_min
                y_u= y_max
      endIF

         RETURN
      END SUBROUTINE y1DIS_lim