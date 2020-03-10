Option Explicit

Sub rmv()

'remove brackets
Dim i, ending As Integer
Dim cel As String

ending = Range("D1").End(xlDown).Row

For i = 2 To ending
    cel = Cells(i, 4).Text
    cel = Mid(cel, 2, Len(cel) - 2)
    Cells(i, 4) = cel
Next i

End Sub
Sub split()

Dim txt, detected As String
Dim arr
Dim startstr, beamstr, endstr As String
Dim i, j, nbr, ending As Integer
ending = Range("D1").End(xlDown).Row

i = 2
Do Until Cells(i, 4).Offset(1, 0).Text = ""
    txt = Cells(i, 4).Text
    arr = VBA.split(txt, ", ")
    nbr = UBound(arr)
    detected = arr(0)
    Cells(i, 4) = detected
    If nbr <> 0 Then
        startstr = Cells(i, 1).Text
        endstr = Cells(i, 2).Text
        beamstr = Cells(i, 3).Text
        For j = 1 To nbr
            Rows(i + j & ":" & i + j).Select
            Selection.insert Shift:=xlDown, CopyOrigin:=xlFormatFromLeftOrAbove
            detected = arr(j)
            Cells(i + j, 1) = startstr
            Cells(i + j, 2) = endstr
            Cells(i + j, 3) = beamstr
            Cells(i + j, 4) = detected
        Next j
        i = i + nbr
    End If
    i = i + 1
Loop
'identify and split lists 1 value per row

End Sub

Sub extravals()

Dim first, final, tot As Integer
Dim i, k, ending As Integer
'for each value insert 599 new rows with diff start time

k = 2
Do Until Cells(k - 1, 4).Offset(1, 0).Text = ""
        first = Cells(k, 1)
        final = Cells(k, 2)
        tot = final - first
            For i = 1 To (tot - 1)
            'insert row
                Rows(k + i & ":" & k + i).Select
                Selection.insert Shift:=xlDown, CopyOrigin:=xlFormatFromLeftOrAbove
                Cells(k + i, 1) = first + i
                Cells(k + i, 3) = Cells(k, 3)
                Cells(k + i, 4) = Cells(k, 4)
            Next i
    k = k + tot
Loop

End Sub

----------------------------------

by_beam <- function(dat) {
  freq <- dat$detected
  time <- dat$start
  beam <- dat$beam
  main <- paste("variation in harmonic over time, colour-coded by beam", sep=" ")
  p <- ggplot(dat, aes(freq, time), group=beam) + ggtitle(main) + geom_point(aes(color = beam), size = 0.7) + 
    scale_color_viridis(discrete=FALSE, option = "D", direction=-1) +
    theme_black() + labs(x = "frequency (Hz)", y = "time (sec)")
  p <- ggplotly(p)
  p
}
