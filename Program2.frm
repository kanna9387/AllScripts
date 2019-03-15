VERSION 5.00
Begin VB.Form Program2 
   Caption         =   "Form1"
   ClientHeight    =   4905
   ClientLeft      =   3540
   ClientTop       =   4440
   ClientWidth     =   10245
   LinkTopic       =   "Form1"
   ScaleHeight     =   4905
   ScaleWidth      =   10245
   Begin VB.TextBox TB1 
      Height          =   375
      Left            =   2880
      TabIndex        =   3
      Top             =   600
      Width           =   1575
   End
   Begin VB.TextBox TB2 
      Height          =   375
      Left            =   2880
      TabIndex        =   4
      Top             =   1320
      Width           =   1575
   End
   Begin VB.TextBox TB3 
      BackColor       =   &H8000000B&
      Height          =   375
      Left            =   2880
      TabIndex        =   5
      Top             =   2160
      Width           =   1575
   End
   Begin VB.Frame Frame1 
      Caption         =   "Frame1"
      Height          =   3855
      Left            =   5520
      TabIndex        =   6
      Top             =   480
      Width           =   4095
      Begin VB.CommandButton btn_mul 
         Caption         =   "Multiply"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   9.75
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   495
         Left            =   360
         TabIndex        =   9
         Top             =   1920
         Width           =   1095
      End
      Begin VB.CommandButton btn_sub 
         Caption         =   "Sub"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   9.75
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   495
         Index           =   0
         Left            =   2280
         TabIndex        =   8
         Top             =   480
         Width           =   1215
      End
      Begin VB.CommandButton btn_ADD 
         Caption         =   "ADD"
         BeginProperty Font 
            Name            =   "MS Sans Serif"
            Size            =   9.75
            Charset         =   0
            Weight          =   700
            Underline       =   0   'False
            Italic          =   0   'False
            Strikethrough   =   0   'False
         EndProperty
         Height          =   495
         Index           =   0
         Left            =   360
         TabIndex        =   7
         Top             =   480
         Width           =   975
      End
   End
   Begin VB.Label Results 
      BackColor       =   &H80000006&
      BorderStyle     =   1  'Fixed Single
      Caption         =   "Results"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   12
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      ForeColor       =   &H8000000B&
      Height          =   495
      Index           =   2
      Left            =   480
      TabIndex        =   2
      Top             =   2040
      Width           =   2175
   End
   Begin VB.Label EnterName2 
      BackColor       =   &H8000000D&
      BorderStyle     =   1  'Fixed Single
      Caption         =   "Enter Name 2"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   9.75
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   495
      Index           =   1
      Left            =   480
      TabIndex        =   1
      Top             =   1320
      Width           =   2175
   End
   Begin VB.Label EnterName1 
      BackColor       =   &H8000000D&
      BorderStyle     =   1  'Fixed Single
      Caption         =   "Enter Name 1"
      BeginProperty Font 
         Name            =   "MS Sans Serif"
         Size            =   9.75
         Charset         =   0
         Weight          =   700
         Underline       =   0   'False
         Italic          =   0   'False
         Strikethrough   =   0   'False
      EndProperty
      Height          =   495
      Index           =   0
      Left            =   480
      TabIndex        =   0
      Top             =   600
      Width           =   2175
   End
End
Attribute VB_Name = "Program2"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = False
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False

Private Sub btn_ADD_Click(Index As Integer)
Dim A As Integer
Dim B As Integer

A = Val(TB1.Text)
B = Val(TB2.Text)

TB3.Text = A + B
End Sub

Private Sub btn_mul_Click()
Dim A As Integer
Dim B As Integer

A = Val(TB1.Text)
B = Val(TB2.Text)

TB3.Text = A * B
End Sub

Private Sub btn_sub_Click(Index As Integer)
Dim A As Integer
Dim B As Integer

A = Val(TB1.Text)
B = Val(TB2.Text)

TB3.Text = A - B
End Sub
