************************************************************************
      FUNCTION FunGeM(var)
************************************************************************
*                                                                      *
*                                                                      *
************************************************************************

         USE Routines

         REAL FunGeM,GeM_FQCD_L,var,x,Q2,E_nu,F1,F2,F3,F4,F5,F6,
     #        Uq,Ua,Dq,Da,Sq,Sa,Cq,Ca,G,A,f

         SAVE

         COMMON            /x/x                                          Bjorken scaling variable x
         COMMON           /Q2/Q2                                         Square of mometum transfer (Q^2=-q^2)
         COMMON         /E_nu/E_nu                                       Neutrino energy

         DIMENSION f(-6:6)

         FunGeM= one
         RETURN

*     ================================================================ *
      ENTRY GeM_FQCD_L(var)
*     ================================================================ *
         CALL SFCC(E_nu,var,Q2,F1,F2,F3,F4,F5,F6)
*        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*        PREVIOUS METHOD BASED ON CERN PDFLIB LIBRARY
*        CALL PDF (E_nu,var,Q2,Uq,Ua,Dq,Da,Sq,Sa,Cq,Ca,G,A)
*        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
*        CURRENT METHOD BASEN ON LHAPDF PACKAGE
         CALL evolvePDF(var,sqrt(Q2),f)
         g = f(+0)
         Uq= f(+2); Dq= f(+1); Sq= f(+3); Cq= f(+4)
         Ua= f(-2); Da= f(-1); Sa= f(-3); Ca= f(-4)
         A = alphasPDF(sqrt(Q))
*        - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - *
         GeM_FQCD_L= A*(8*F2/3+16*(var-x)*G)/var
         RETURN

      END FUNCTION FunGeM