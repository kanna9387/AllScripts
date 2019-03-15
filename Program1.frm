VERSION 5.00
Begin VB.Form Program1 
   Caption         =   "Form1"
   ClientHeight    =   3030
   ClientLeft      =   7395
   ClientTop       =   3120
   ClientWidth     =   4560
   LinkTopic       =   "Form1"
   ScaleHeight     =   3030
   ScaleWidth      =   4560
   Begin VB.CommandButton HI 
      Appearance      =   0  'Flat
      Caption         =   "HI"
      Height          =   495
      Left            =   840
      TabIndex        =   0
      Top             =   840
      Width           =   1455
   End
   Begin VB.Menu Program1 
      Caption         =   "Program-1"
      Index           =   1
   End
End
Attribute VB_Name = "Program1"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False

Private Sub HI_Click()
    MsgBox ("Hello")
End Sub
