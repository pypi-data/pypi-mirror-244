************************************************************************
      SUBROUTINE xDIS_lim(E_nu,x_min,x_max)
************************************************************************
*                                                                      *
*                                                                      *
************************************************************************

         USE PhysMathConstants, ONLY: one

         IMPLICIT REAL*8 (A-Z)

         COMMON      /m_ini/m_ini,mm_ini                                 Mass of target nucleon
         COMMON      /m_lep/m_lep,mm_lep                                 Mass of final charged lepton
         COMMON      /m_fin/m_fin,mm_fin                                 Mass of final hadron or hadron system

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
      endIF

         RETURN
      END SUBROUTINE xDIS_lim

************************************************************************
      SUBROUTINE yDIS_lim(E_nu,x,y_min,y_max)
************************************************************************
*                                                                      *
*                                                                      *
************************************************************************

         USE PhysMathConstants, ONLY: one

         IMPLICIT REAL*8 (A-Z)

         COMMON      /m_ini/m_ini,mm_ini                                 Mass of target nucleon
         COMMON      /m_lep/m_lep,mm_lep                                 Mass of final charged lepton
         COMMON      /m_fin/m_fin,mm_fin                                 Mass of final hadron or hadron system

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

         RETURN
      END SUBROUTINE yDIS_lim

************************************************************************
      SUBROUTINE W2DIS_lim(E_nu,W2_min,W2_max)
************************************************************************
*                                                                      *
*                                                                      *
************************************************************************

         IMPLICIT REAL*8 (A-Z)

         COMMON      /m_ini/m_ini,mm_ini                                 Mass of target nucleon
         COMMON      /m_lep/m_lep,mm_lep                                 Mass of final charged lepton
         COMMON      /m_fin/m_fin,mm_fin                                 Mass of final hadron or hadron system

         W2_min= max(mm_fin,mm_ini)
         W2_max= (sqrt(mm_ini+2*m_ini*E_nu)-m_lep)**2

         RETURN
      END SUBROUTINE W2DIS_lim

************************************************************************
      SUBROUTINE Q2DIS_lim(E_nu,W2,Q2_min,Q2_max)
************************************************************************
*                                                                      *
*                                                                      *
************************************************************************

         USE PhysMathConstants, ONLY: zero

         IMPLICIT REAL*8 (A-Z)

         COMMON      /m_ini/m_ini,mm_ini                                 Mass of target nucleon
         COMMON      /m_lep/m_lep,mm_lep                                 Mass of final charged lepton

         s      = mm_ini+2*m_ini*E_nu
         Ecm_nu = (s-mm_ini   )/(2*sqrt(s))
         Ecm_lep= (s+mm_lep-W2)/(2*sqrt(s))
         IF (Ecm_lep**2-mm_lep.le.zero) THEN
           Pcm_lep= zero
                                        ELSE
           Pcm_lep= sqrt(Ecm_lep**2-mm_lep)
      endIF
         Q2_min= mm_lep*2*Ecm_nu/(Ecm_lep+Pcm_lep)-mm_lep
         Q2_max=        2*Ecm_nu*(Ecm_lep+Pcm_lep)-mm_lep

         RETURN
      END SUBROUTINE Q2DIS_lim
