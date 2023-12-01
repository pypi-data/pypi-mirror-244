************************************************************************
      FUNCTION Rset_Liang(x,Q2)
************************************************************************
*                                                                      *
*                                                                      *
************************************************************************

         USE InpOutUnits
         USE PhysMathConstants, ONLY: one,mm_I

         IMPLICIT REAL*8 (A-H,K-N,O-Z), INTEGER (I,J)

         INTEGER i,j
            REAL Rset_Liang,R_Liang,x,Q2,stepWW,stepQQ,WW,QQ,z,R,W2,
     #           R_E143,F2,F1,FL,Sp2,m_ini,mm_ini,
     #           F,C,RWW_R,RWW_A

         SAVE

         LOGICAL(2),PARAMETER::
     #              Quiz= .TRUE.,                                        Coeff2 settings
     #              TEST= .FALSE.                                        Test for spline interpolation
            INTEGER,PARAMETER::
     #              NQQ = 1000, NWW = 100,                               Number of reference points
     #              MQQ =   10, MWW = 500,                               Number of arbitrary points
     #              Mode=    1, L   =   1                                Coeff2 settings
               REAL,PARAMETER::
     #              QQ_ini=0.30, QQ_fin=5.00,
     #              WW_ini=1.00, WW_fin=4.00

         COMMON /m_ini/m_ini,mm_ini                                      Mass of target nucleon [GeV, GeV^2]

         DIMENSION RWW_R(NQQ),RWW_A(MQQ),F(NWW,NQQ),C((NWW+2)*(NQQ+2))

c        OPEN(Ndat01,FILE=OutR//'RW2/RW2_Liang_rp.dat')
         stepWW= (WW_fin-WW_ini)/(NWW-1)
         stepQQ= (QQ_fin-QQ_ini)/(NQQ-1)
         DO i= 1,NWW
           WW= WW_ini+(i-1)*stepWW
           DO j= 1,NQQ
             QQ= QQ_ini+(j-1)*stepQQ
             IF (WW.lt.1.15 .or. WW.gt.3.90 .or.
     #           QQ.lt.0.30 .or. QQ.gt.5.00     ) THEN
               z= QQ/(QQ-mm_I+WW)
               R= R_E143(z,QQ,1,0)
                                                  ELSE
               CALL SFmodel_Liang(QQ,WW,R,F2,F1,FL)
          endIF
             F(i,j)= R
             RWW_R(j)= R
        endDO
c          WRITE(Ndat01,101) WW, (RWW_R(j), j=1,NQQ)
      endDO
c        CLOSE(Ndat01)
         CALL Coeff2(Mode,1,NWW,NQQ,WW_ini,QQ_ini,WW_fin,QQ_fin,
     #               F,C,Quiz,L)
         IF (TEST) THEN
           OPEN(Ndat01,FILE=OutSF//'R/RW2/RW2_Liang_ap.dat')
           stepWW= (WW_fin-WW_ini)/(MWW-1)
           stepQQ= (QQ_fin-QQ_ini)/(MQQ-1)
           DO i= 1,MWW
             WW= WW_ini+(i-1)*stepWW
             DO j= 1,MQQ
               QQ= QQ_ini+(j-1)*stepQQ
               RWW_A(j)= Sp2(1,C,WW,QQ)
          endDO
             WRITE(Ndat01,102) WW, (RWW_A(j), j=1,MQQ)
        endDO
           CLOSE(Ndat01)
      endIF

         Rset_Liang= one
         RETURN

  101 FORMAT(1PE9.3,1100(1PE10.3))                                       GNU FORTRAN Compiler
  102 FORMAT(1PE9.3,1100(1PE10.3))                                       GNU FORTRAN Compiler

*     ==================================================================
      ENTRY R_Liang(x,Q2)
*     ==================================================================
         W2= Q2*(1-x)/x+mm_ini
         IF (W2.lt.WW_ini .or. W2.gt.WW_fin .or.
     #       Q2.lt.QQ_ini .or. Q2.gt.QQ_fin     ) THEN
           R_Liang= R_E143(x,Q2,1,0)
                                                  ELSE
           R_Liang= Sp2(1,C,W2,Q2)
      endIF
         RETURN
*     ==================================================================

      END FUNCTION Rset_Liang
