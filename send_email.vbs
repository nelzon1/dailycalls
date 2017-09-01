Const PR_ATTACH_MIME_TAG = "http://schemas.microsoft.com/mapi/proptag/0x370E001E"
Const PR_ATTACH_CONTENT_ID = "http://schemas.microsoft.com/mapi/proptag/0x3712001E"
Const PR_ATTACHMENT_HIDDEN = "http://schemas.microsoft.com/mapi/proptag/0x7FFE000B"


Sub testing2()
Dim ToAddress
Dim FromAddress
Dim MessageSubject
Dim MyTime
Dim objFileToRead
Dim RunDate
Dim MessageBody
Dim MessageAttachment
Dim ol, ns, newMail
Dim realAttachment
MyTime = Date

Set objFileToRead = CreateObject("Scripting.FileSystemObject").OpenTextFile("C:\coding\dailycalls\date.txt",1)
RunDate = objFileToRead.ReadAll()
objFileToRead.Close
Set objFileToRead = Nothing

ToAddress = "ActiveNetSupportInternal@activenetwork.com"
MessageSubject = RunDate
MessageBody = "Stats Attached" & vbCrLf & "Produced at " & MyTime
MessageAttachment = "C:\coding\Agent Queue Analysis\daily_calls.png"

Set objOutlook = CreateObject("Outlook.Application")
'Set ns = objOutlook.GetNamespace("MAPI")
Set newMail = objOutlook.CreateItem(olMailItem)
newMail.Subject = MessageSubject
newMail.Body = ""
newMail.Recipients.Add (ToAddress)
newMail.Recipients.Add ("jake.nelson@activenetwork.com")
'newMail.CC = "jake.nelson@activenetwork"
Set realAttachment = newMail.Attachments.Add(MessageAttachment)
Set oPA = realAttachment.PropertyAccessor
oPA.SetProperty PR_ATTACH_MIME_TAG, "image/jpeg"
oPA.SetProperty PR_ATTACH_CONTENT_ID, "myident" 'change myident for another other image
newMail.HTMLBody = newMail.HTMLBody & "<IMG align=baseline border=0 hspace=0 src=cid:myident>" 'need to match the "myident" above
newMail.Send
Set objMail = Nothing
Set objOutlook = Nothing
End Sub


testing2()
