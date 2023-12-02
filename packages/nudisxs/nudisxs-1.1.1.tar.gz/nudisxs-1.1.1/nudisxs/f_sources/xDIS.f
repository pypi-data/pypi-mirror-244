************************************************************************
      SUBROUTINE x1DIS_lim(E_nu,x_min,x_max)
************************************************************************
*                                                                      *
*                                                                      *
************************************************************************

         USE PhysMathConstants, ONLY: zero,one

         IMPLICIT REAL*8 (A-Z)

         COMMON      /m_ini/m_ini,mm_ini                                 Mass of target nucleon
         COMMON      /m_lep/m_lep,mm_lep                                 Mass of final charged lepton
         COMMON      /m_fin/m_fin,mm_fin                                 Mass of final hadron or hadron system
         COMMON     /x_limit/x_l,x_u

         x_min= zero
         x_max= one
         IF (m_ini.eq.m_fin) THEN
           x_min= mm_lep/(2*m_ini*(E_nu-m_lep))
           x_max= one
                             ELSE
           a    = one-(mm_fin-mm_ini-mm_lep)*
     #            ((mm_fin-mm_ini)*E_nu+mm_lep*m_ini)/
     #            (2*m_ini*E_nu**2*(mm_fin-mm_ini))
           b    = sqrt((one-((m_fin-m_lep)**2-mm_ini)/(2*m_ini*E_nu))*
     #                 (one-((m_fin+m_lep)**2-mm_ini)/(2*m_ini*E_nu)))
           c    = one+(mm_fin-mm_ini-mm_lep)**2/
     #            (4*(mm_fin-mm_ini)*E_nu**2)
           x_min= (a-b)/(2*c)
           x_max= (a+b)/(2*c)
           x_l  = x_min
           x_u  = x_max
      endIF
         IF (x_min<zero .or. x_max<zero) THEN
                x_l= zero
                x_u= zero
                                         ELSE
                x_l= x_min
                x_u= x_max
      endIF

         RETURN
      END SUBROUTINE x1DIS_lim