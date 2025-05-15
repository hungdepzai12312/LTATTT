from libratom.lib.pff import PffArchive

filename = "Ex.pst"
archive = PffArchive(filename)

for folder in archive.folders():
    if folder.get_number_of_sub_messages() != 0:
        for message in folder.sub_messages:
            print("Sender: %s" % message.get_sender_name())
            print("Subject: %s" % message.get_subject())
            print("Message: %s\n" % message.get_plain_text_body())
            #write a keylogger using python
            #protecting against email collection
            