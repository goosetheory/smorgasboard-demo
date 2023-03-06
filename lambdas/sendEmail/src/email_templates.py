homepage_link = 'https://smorgasboard.io'
get_started_link = 'https://smorgasboard.io/get-started'
create_board_link = 'https://smorgasboard.io/create-board'
all_boards_link = 'https://smorgasboard.io/boards'
contact_us_link = 'https://smorgasboard.io/contact-us'
free_trial_link = 'https://smorgasboard.io/free-trial'

def board_ended_subject():
	return 'Your SmorgasBoard photos are ready!'

def board_ended_body_text(given_name, board_name, join_code):
	archive_link = f'https://smorgasboard.io/archive/{join_code}'

	return f'''
Dear {given_name},

Thanks so much for using SmorgasBoard. We hope your event was a big success.

Your board, {board_name}, has completed. You can now access your photos here:

{archive_link}

We'll keep these photos for up to three months. Please make sure to download them soon! If you have any questions or feedback (positive or negative!), please feel free to reach out to sam@smorgasboard.io. We love hearing from you!

One more thing: if you liked SmorgasBoard, tell a friend about us! We're a small, independent business, and your support means a lot.
'''

def board_ended_body_html(given_name, board_name, join_code):
	archive_link = f'https://smorgasboard.io/archive/{join_code}'

	return f'''
	<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd">
<html>
<head>
    <!-- Compiled with Bootstrap Email version: 1.0.1 -->
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">

          <style type="text/css">
            body,table,td{{font-family:Helvetica,Arial,sans-serif !important}}.ExternalClass{{width:100%}}.ExternalClass,.ExternalClass p,.ExternalClass span,.ExternalClass font,.ExternalClass td,.ExternalClass div{{line-height:150%}}a{{text-decoration:none}}*{{color:inherit}}a[x-apple-data-detectors],u+#body a,#MessageViewBody a{{color:inherit;text-decoration:none;font-size:inherit;font-family:inherit;font-weight:inherit;line-height:inherit}}img{{-ms-interpolation-mode:bicubic}}table:not([class^=s-]){{font-family:Helvetica,Arial,sans-serif;mso-table-lspace:0pt;mso-table-rspace:0pt;border-spacing:0px;border-collapse:collapse}}table:not([class^=s-]) td{{border-spacing:0px;border-collapse:collapse}}@media screen and (max-width: 600px){{.w-full,.w-full>tbody>tr>td{{width:100% !important}}.w-48,.w-48>tbody>tr>td{{width:192px !important}}.pt-2:not(table),.pt-2:not(.btn)>tbody>tr>td,.pt-2.btn td a,.py-2:not(table),.py-2:not(.btn)>tbody>tr>td,.py-2.btn td a{{padding-top:8px !important}}.pb-2:not(table),.pb-2:not(.btn)>tbody>tr>td,.pb-2.btn td a,.py-2:not(table),.py-2:not(.btn)>tbody>tr>td,.py-2.btn td a{{padding-bottom:8px !important}}.pr-4:not(table),.pr-4:not(.btn)>tbody>tr>td,.pr-4.btn td a,.px-4:not(table),.px-4:not(.btn)>tbody>tr>td,.px-4.btn td a{{padding-right:16px !important}}.pl-4:not(table),.pl-4:not(.btn)>tbody>tr>td,.pl-4.btn td a,.px-4:not(table),.px-4:not(.btn)>tbody>tr>td,.px-4.btn td a{{padding-left:16px !important}}*[class*=s-lg-]>tbody>tr>td{{font-size:0 !important;line-height:0 !important;height:0 !important}}}}

          </style>
</head>
<body class="bg-dark" style="outline: 0; width: 100%; min-width: 100%; height: 100%; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; font-family: Helvetica, Arial, sans-serif; line-height: 24px; font-weight: normal; font-size: 16px; -moz-box-sizing: border-box; -webkit-box-sizing: border-box; box-sizing: border-box; color: #000000; margin: 0; padding: 0; border: 0;" bgcolor="#1a202c"><table class="bg-dark body" valign="top" role="presentation" border="0" cellpadding="0" cellspacing="0" style="outline: 0; width: 100%; min-width: 100%; height: 100%; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; font-family: Helvetica, Arial, sans-serif; line-height: 24px; font-weight: normal; font-size: 16px; -moz-box-sizing: border-box; -webkit-box-sizing: border-box; box-sizing: border-box; color: #000000; margin: 0; padding: 0; border: 0;" bgcolor="#1a202c">
  <tbody>
    <tr>
      <td valign="top" style="line-height: 24px; font-size: 16px; margin: 0;" align="left" bgcolor="#1a202c">

	<table class="px-4 bg-dark w-full" role="presentation" border="0" cellpadding="0" cellspacing="0" style="width: 100%;" bgcolor="#1a202c" width="100%">
  <tbody>
    <tr>
      <td style="line-height: 24px; font-size: 16px; width: 100%; padding-right: 16px; padding-left: 16px; margin: 0;" align="left" bgcolor="#1a202c" width="100%">

		<a href="https://smorgasboard.io" style="color: #0d6efd;">
			<table class="ax-center" role="presentation" align="center" border="0" cellpadding="0" cellspacing="0" style="margin: 0 auto;">
  <tbody>
    <tr>
      <td style="line-height: 24px; font-size: 16px; margin: 0;" align="left">
        <img class="w-48" style="height: auto; line-height: 100%; outline: none; text-decoration: none; display: block; width: 192px; padding: 4px; border: 0 none;" src="https://smorgasboard.io/assets/logo-color.png" width="192">
      </td>
    </tr>
  </tbody>
</table>
		</a>
		<table class="py-2 bg-dark border-0 rounded-md w-full" role="presentation" border="0" cellpadding="0" cellspacing="0" style="border-radius: 6px; width: 100%; border: 0px solid #e2e8f0;" bgcolor="#1a202c" width="100%">
  <tbody>
    <tr>
      <td style="line-height: 24px; font-size: 16px; border-radius: 6px; width: 100%; padding-top: 8px; padding-bottom: 8px; margin: 0;" align="left" bgcolor="#1a202c" width="100%">

			<table class="card" role="presentation" border="0" cellpadding="0" cellspacing="0" style="border-radius: 6px; border-collapse: separate !important; width: 100%; overflow: hidden; border: 1px solid #e2e8f0;" bgcolor="#e1e1e1">
  <tbody>
    <tr>
      <td style="line-height: 24px; font-size: 16px; width: 100%; margin: 0;" align="left" bgcolor="#ffffff">

				<table class="card-body" role="presentation" border="0" cellpadding="0" cellspacing="0" style="width: 100%;">
  <tbody>
    <tr>
      <td style="line-height: 24px; font-size: 16px; width: 100%; margin: 0; padding: 20px;" align="left">

					<p style="line-height: 24px; font-size: 16px; width: 100%; margin: 0;" align="left">
						Dear {given_name},
					</p>
					<br>
					<p style="line-height: 24px; font-size: 16px; width: 100%; margin: 0;" align="left">
						Thanks so much for using SmorgasBoard. We hope your event was a big success.
					</p>
					<br>
					<p style="line-height: 24px; font-size: 16px; width: 100%; margin: 0;" align="left">
						Your board, {board_name}, has completed. You can now access your photos <a href="{archive_link}" style="color: #0d6efd;">here</a>.
					</p>
					<br>
					<p style="line-height: 24px; font-size: 16px; width: 100%; margin: 0;" align="left">
						We'll keep these photos for up to three months. Please make sure to download them soon! If you have any questions or feedback (positive or negative!), please get in touch at our <a href="{contact_us_link}" style="color: #0d6efd;">contact page</a>. We love hearing from you!
					</p>
					<br>
					<p style="line-height: 24px; font-size: 16px; width: 100%; margin: 0;" align="left">
						One more thing: if you liked SmorgasBoard, tell a friend about us! We're a small, independent business, and your support means a lot.
					</p>

      </td>
    </tr>
  </tbody>
</table>

      </td>
    </tr>
  </tbody>
</table>

      </td>
    </tr>
  </tbody>
</table>

      </td>
    </tr>
  </tbody>
</table>

      </td>
    </tr>
  </tbody>
</table></body>
</html>
'''


def free_trial_ended_subject():
	return 'Thanks from SmorgasBoard!'

def free_trial_ended_body_text(given_name):
	return f'''
Dear {given_name},


Thanks for trying SmorgasBoard! We hope you enjoyed your free trial.


Using our paid version is just as easy, and includes additional benefits like

- A digital photo album delivered to your inbox after your event ends
- 48 hours of use
- Unlimited photo uploads
- Unlimited guests
- Priority support from a human (no robots!)
- Satisfaction guaranteed or your money back

all for under a hundred dollars. That's way cheaper than the next photo booth.

We hope you'll keep us in mind for your next event. Please feel free to reach out if you have any questions!
'''


def free_trial_ended_body_html(given_name):
	return f'''
	<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd">
<html>
  <head>
    <!-- Compiled with Bootstrap Email version: 1.1.0 --><meta http-equiv="x-ua-compatible" content="ie=edge">
    <meta name="x-apple-disable-message-reformatting">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="format-detection" content="telephone=no, date=no, address=no, email=no">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    <style type="text/css">
      body,table,td{{font-family:Helvetica,Arial,sans-serif !important}}.ExternalClass{{width:100%}}.ExternalClass,.ExternalClass p,.ExternalClass span,.ExternalClass font,.ExternalClass td,.ExternalClass div{{line-height:150%}}a{{text-decoration:none}}*{{color:inherit}}a[x-apple-data-detectors],u+#body a,#MessageViewBody a{{color:inherit;text-decoration:none;font-size:inherit;font-family:inherit;font-weight:inherit;line-height:inherit}}img{{-ms-interpolation-mode:bicubic}}table:not([class^=s-]){{font-family:Helvetica,Arial,sans-serif;mso-table-lspace:0pt;mso-table-rspace:0pt;border-spacing:0px;border-collapse:collapse}}table:not([class^=s-]) td{{border-spacing:0px;border-collapse:collapse}}@media screen and (max-width: 600px){{.w-full,.w-full>tbody>tr>td{{width:100% !important}}.w-48,.w-48>tbody>tr>td{{width:192px !important}}.pt-2:not(table),.pt-2:not(.btn)>tbody>tr>td,.pt-2.btn td a,.py-2:not(table),.py-2:not(.btn)>tbody>tr>td,.py-2.btn td a{{padding-top:8px !important}}.pb-2:not(table),.pb-2:not(.btn)>tbody>tr>td,.pb-2.btn td a,.py-2:not(table),.py-2:not(.btn)>tbody>tr>td,.py-2.btn td a{{padding-bottom:8px !important}}.pr-4:not(table),.pr-4:not(.btn)>tbody>tr>td,.pr-4.btn td a,.px-4:not(table),.px-4:not(.btn)>tbody>tr>td,.px-4.btn td a{{padding-right:16px !important}}.pl-4:not(table),.pl-4:not(.btn)>tbody>tr>td,.pl-4.btn td a,.px-4:not(table),.px-4:not(.btn)>tbody>tr>td,.px-4.btn td a{{padding-left:16px !important}}*[class*=s-lg-]>tbody>tr>td{{font-size:0 !important;line-height:0 !important;height:0 !important}}
    </style>
  </head>
  <body class="bg-dark" style="outline: 0; width: 100%; min-width: 100%; height: 100%; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; font-family: Helvetica, Arial, sans-serif; line-height: 24px; font-weight: normal; font-size: 16px; -moz-box-sizing: border-box; -webkit-box-sizing: border-box; box-sizing: border-box; color: #000000; margin: 0; padding: 0; border: 0;" bgcolor="#1a202c">
    <table class="bg-dark body" valign="top" role="presentation" border="0" cellpadding="0" cellspacing="0" style="outline: 0; width: 100%; min-width: 100%; height: 100%; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; font-family: Helvetica, Arial, sans-serif; line-height: 24px; font-weight: normal; font-size: 16px; -moz-box-sizing: border-box; -webkit-box-sizing: border-box; box-sizing: border-box; color: #000000; margin: 0; padding: 0; border: 0;" bgcolor="#1a202c">
      <tbody>
        <tr>
          <td valign="top" style="line-height: 24px; font-size: 16px; margin: 0;" align="left" bgcolor="#1a202c">
            <table class="px-4 bg-dark w-full" role="presentation" border="0" cellpadding="0" cellspacing="0" style="width: 100%;" bgcolor="#1a202c" width="100%">
              <tbody>
                <tr>
                  <td style="line-height: 24px; font-size: 16px; width: 100%; padding-right: 16px; padding-left: 16px; margin: 0;" align="left" bgcolor="#1a202c" width="100%">
                    <a href="https://smorgasboard.io" style="color: #0d6efd;">
                      <table class="ax-center" role="presentation" align="center" border="0" cellpadding="0" cellspacing="0" style="margin: 0 auto;">
                        <tbody>
                          <tr>
                            <td style="line-height: 24px; font-size: 16px; margin: 0;" align="left">
                              <img class="w-48" style="height: auto; line-height: 100%; outline: none; text-decoration: none; display: block; width: 192px; padding: 4px; border: 0 none;" src="https://smorgasboard.io/assets/logo-color.png" width="192">
                            </td>
                          </tr>
                        </tbody>
                      </table>
                    </a>
                    <table class="py-2 bg-dark border-0 rounded-md w-full" role="presentation" border="0" cellpadding="0" cellspacing="0" style="border-radius: 6px; width: 100%; border: 0px solid #e2e8f0;" bgcolor="#1a202c" width="100%">
                      <tbody>
                        <tr>
                          <td style="line-height: 24px; font-size: 16px; border-radius: 6px; width: 100%; padding-top: 8px; padding-bottom: 8px; margin: 0;" align="left" bgcolor="#1a202c" width="100%">
                            <table class="card" role="presentation" border="0" cellpadding="0" cellspacing="0" style="border-radius: 6px; border-collapse: separate !important; width: 100%; overflow: hidden; border: 1px solid #e2e8f0;" bgcolor="#e1e1e1">
                              <tbody>
                                <tr>
                                  <td style="line-height: 24px; font-size: 16px; width: 100%; margin: 0;" align="left" bgcolor="#ffffff">
                                    <table class="card-body" role="presentation" border="0" cellpadding="0" cellspacing="0" style="width: 100%;">
                                      <tbody>
                                        <tr>
                                          <td style="line-height: 24px; font-size: 16px; width: 100%; margin: 0; padding: 20px;" align="left">
                                            <p style="line-height: 24px; font-size: 16px; width: 100%; margin: 0;" align="left">
                                              Dear {given_name},
                                            </p>
                                            <br>
                                            <p style="line-height: 24px; font-size: 16px; width: 100%; margin: 0;" align="left">
                                              Thanks for trying SmorgasBoard! We hope you enjoyed your free trial.
                                            </p>
                                            <br>
                                            <p style="line-height: 24px; font-size: 16px; width: 100%; margin: 0;" align="left">
                                              Using our <a href="{get_started_link}" style="color: #0d6efd;">paid version</a> is just as easy, and includes additional benefits like
                                            </p>
                                            <ul>
                                              <li style="margin-left: -1rem;">
                                                A digital photo album delivered to your inbox after your event ends
                                              </li>
                                              <li style="margin-left: -1rem;">
                                                48 hours of use
                                              </li>
                                              <li style="margin-left: -1rem;">
                                                Unlimited photo uploads
                                              </li>
                                              <li style="margin-left: -1rem;">
                                                Unlimited guests
                                              </li>
                                              <li style="margin-left: -1rem;">
                                                Priority support from a human (no robots!)
                                              </li>
                                              <li style="margin-left: -1rem;">
                                                Satisfaction guaranteed or your money back
                                              </li>
                                            </ul>
                                            <p style="line-height: 24px; font-size: 16px; width: 100%; margin: 0;" align="left">
                                              all for <b>under a hundred dollars</b>. That's way cheaper than the next photo booth.
                                            </p>
                                            <br>
                                            <p style="line-height: 24px; font-size: 16px; width: 100%; margin: 0;" align="left">
                                              We hope you'll keep us in mind for your next event. Please feel free to <a href="{contact_us_link}" style="color: #0d6efd;">reach out</a> if you have any questions!
                                            </p>
                                          </td>
                                        </tr>
                                      </tbody>
                                    </table>
                                  </td>
                                </tr>
                              </tbody>
                            </table>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </td>
                </tr>
              </tbody>
            </table>
          </td>
        </tr>
      </tbody>
    </table>
  </body>
</html>
'''



def board_purchased_subject():
	return 'Thanks from SmorgasBoard!'


def board_purchased_body_text(given_name):
	return f'''
Dear {given_name},

Thanks for your purchase. We're glad you've chosen us for your next event.

Here are some more details on how to use SmorgasBoard.

Before your event:
- Your board is where all your photos will be shown, and also has a QR code for guests to scan when they want to add a photo. Give it a fun name, if you haven't already! You can do that here: {create_board_link}
- Make sure you'll be able to display your board on the day of your event. Your venue will need a TV or projector you can connect a computer to. You'll also need an internet connection so you can display photos as you and your guests add them.


Day-of:
- Connect your computer to the internet, and hook it up to your venue's TV/projector. Connect it to your venue's wifi and navigate to your board: {all_boards_link}
- Click the "Launch Board" button when you're ready to start the board. You'll be able to add photos for 48 hours. Then, click the "Open Board" button to show the board fullscreen on your TV/projector. You'll see an empty board with a QR code.
- Let your guests know they can scan the QR code with their phones to take a photo.


After the event:
- Look for an email from us for digital copies of your photos. It should arrive within a day or two.


If you have any questions, please visit our contact page: {contact_us_link}'''


def board_purchased_body_html(given_name):
	return f'''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd">
<html>
<head>
    <!-- Compiled with Bootstrap Email version: 1.0.1 -->
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">

          <style type="text/css">
            body,table,td{{font-family:Helvetica,Arial,sans-serif !important}}.ExternalClass{{width:100%}}.ExternalClass,.ExternalClass p,.ExternalClass span,.ExternalClass font,.ExternalClass td,.ExternalClass div{{line-height:150%}}a{{text-decoration:none}}*{{color:inherit}}a[x-apple-data-detectors],u+#body a,#MessageViewBody a{{color:inherit;text-decoration:none;font-size:inherit;font-family:inherit;font-weight:inherit;line-height:inherit}}img{{-ms-interpolation-mode:bicubic}}table:not([class^=s-]){{font-family:Helvetica,Arial,sans-serif;mso-table-lspace:0pt;mso-table-rspace:0pt;border-spacing:0px;border-collapse:collapse}}table:not([class^=s-]) td{{border-spacing:0px;border-collapse:collapse}}@media screen and (max-width: 600px){{.w-full,.w-full>tbody>tr>td{{width:100% !important}}.w-48,.w-48>tbody>tr>td{{width:192px !important}}.pt-2:not(table),.pt-2:not(.btn)>tbody>tr>td,.pt-2.btn td a,.py-2:not(table),.py-2:not(.btn)>tbody>tr>td,.py-2.btn td a{{padding-top:8px !important}}.pb-2:not(table),.pb-2:not(.btn)>tbody>tr>td,.pb-2.btn td a,.py-2:not(table),.py-2:not(.btn)>tbody>tr>td,.py-2.btn td a{{padding-bottom:8px !important}}.pr-4:not(table),.pr-4:not(.btn)>tbody>tr>td,.pr-4.btn td a,.px-4:not(table),.px-4:not(.btn)>tbody>tr>td,.px-4.btn td a{{padding-right:16px !important}}.pl-4:not(table),.pl-4:not(.btn)>tbody>tr>td,.pl-4.btn td a,.px-4:not(table),.px-4:not(.btn)>tbody>tr>td,.px-4.btn td a{{padding-left:16px !important}}*[class*=s-lg-]>tbody>tr>td{{font-size:0 !important;line-height:0 !important;height:0 !important}}.s-5>tbody>tr>td{{font-size:20px !important;line-height:20px !important;height:20px !important}}}}

          </style>
</head>
<body class="bg-dark" style="outline: 0; width: 100%; min-width: 100%; height: 100%; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; font-family: Helvetica, Arial, sans-serif; line-height: 24px; font-weight: normal; font-size: 16px; -moz-box-sizing: border-box; -webkit-box-sizing: border-box; box-sizing: border-box; color: #000000; margin: 0; padding: 0; border: 0;" bgcolor="#1a202c"><table class="bg-dark body" valign="top" role="presentation" border="0" cellpadding="0" cellspacing="0" style="outline: 0; width: 100%; min-width: 100%; height: 100%; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; font-family: Helvetica, Arial, sans-serif; line-height: 24px; font-weight: normal; font-size: 16px; -moz-box-sizing: border-box; -webkit-box-sizing: border-box; box-sizing: border-box; color: #000000; margin: 0; padding: 0; border: 0;" bgcolor="#1a202c">
  <tbody>
    <tr>
      <td valign="top" style="line-height: 24px; font-size: 16px; margin: 0;" align="left" bgcolor="#1a202c">

	<table class="bg-dark px-4 w-full" role="presentation" border="0" cellpadding="0" cellspacing="0" style="width: 100%;" bgcolor="#1a202c" width="100%">
  <tbody>
    <tr>
      <td style="line-height: 24px; font-size: 16px; width: 100%; padding-right: 16px; padding-left: 16px; margin: 0;" align="left" bgcolor="#1a202c" width="100%">

		<a href="{homepage_link}" style="color: #0d6efd;">
			<table class="ax-center" role="presentation" align="center" border="0" cellpadding="0" cellspacing="0" style="margin: 0 auto;">
  <tbody>
    <tr>
      <td style="line-height: 24px; font-size: 16px; margin: 0;" align="left">
        <img class="w-48" style="height: auto; line-height: 100%; outline: none; text-decoration: none; display: block; width: 192px; padding: 4px; border: 0 none;" src="https://smorgasboard.io/assets/logo-color.png" width="192">
      </td>
    </tr>
  </tbody>
</table>
		</a>
		<table class="py-2 bg-dark border-0 rounded-md w-full" role="presentation" border="0" cellpadding="0" cellspacing="0" style="border-radius: 6px; width: 100%; border: 0px solid #e2e8f0;" bgcolor="#1a202c" width="100%">
  <tbody>
    <tr>
      <td style="line-height: 24px; font-size: 16px; border-radius: 6px; width: 100%; padding-top: 8px; padding-bottom: 8px; margin: 0;" align="left" bgcolor="#1a202c" width="100%">

			<table class="card" role="presentation" border="0" cellpadding="0" cellspacing="0" style="border-radius: 6px; border-collapse: separate !important; width: 100%; overflow: hidden; border: 1px solid #e2e8f0;" bgcolor="#e1e1e1">
  <tbody>
    <tr>
      <td style="line-height: 24px; font-size: 16px; width: 100%; margin: 0;" align="left" bgcolor="#ffffff">

				<table class="card-body" role="presentation" border="0" cellpadding="0" cellspacing="0" style="width: 100%;">
  <tbody>
    <tr>
      <td style="line-height: 24px; font-size: 16px; width: 100%; margin: 0; padding: 20px;" align="left">

					<p style="line-height: 24px; font-size: 16px; width: 100%; margin: 0;" align="left">
						Dear {given_name},
					</p>
					<br>
					<p style="line-height: 24px; font-size: 16px; width: 100%; margin: 0;" align="left">
						Thanks for your purchase. We're glad you've chosen us for your next event. We're sending along some details on how to use SmorgasBoard to make sure your event is a big success.
					</p>
					<br>
					<p style="line-height: 24px; font-size: 16px; width: 100%; margin: 0;" align="left"><b>Before your event</b></p>
					<ul>
						<li style="margin-left: -1rem;">
							Your board is where all your photos will be shown, and also has a QR code for guests to scan when they want to add a photo. Give it a fun name, if you haven't already! You can do that <a href="{create_board_link}" style="color: #0d6efd;">here</a>.
						</li>
						<li style="margin-left: -1rem;">
							Make sure you'll be able to display your board on the day of your event. Your venue will need a TV or projector you can connect a computer to. You'll also need an internet connection so you can display photos as they're added.
						</li>
					</ul>
					<br>
					<p style="line-height: 24px; font-size: 16px; width: 100%; margin: 0;" align="left"><b>Day-of</b></p>
					<ul>
						<li style="margin-left: -1rem;">
							Connect your computer to the internet, and hook it up to your venue's TV/projector. Connect it to your venue's wifi and navigate to <a href="{all_boards_link}" style="color: #0d6efd;">your board</a>.
						</li>
						<li style="margin-left: -1rem;">
							Click the "Launch Board" button when you're ready to start the board. You'll be able to add photos for 48 hours. Then, click the "Open Board" button to show the board fullscreen on your TV/projector. You'll see an empty board with a QR code.
						</li>
						<li style="margin-left: -1rem;">
							Let your guests know they can scan the QR code with their phones to take a photo.
						</li>
					</ul>
					<br>
					<p style="line-height: 24px; font-size: 16px; width: 100%; margin: 0;" align="left"><b>After the event</b></p>
					<ul>
						<li style="margin-left: -1rem;">
							Look for an email from us for digital copies of your photos. It should arrive within a day or two.
						</li>
					</ul>

					<table class="s-5 w-full" role="presentation" border="0" cellpadding="0" cellspacing="0" style="width: 100%;" width="100%">
  <tbody>
    <tr>
      <td style="line-height: 20px; font-size: 20px; width: 100%; height: 20px; margin: 0;" align="left" width="100%" height="20">
        &#160;
      </td>
    </tr>
  </tbody>
</table>
<table class="hr" role="presentation" border="0" cellpadding="0" cellspacing="0" style="width: 100%;">
  <tbody>
    <tr>
      <td style="line-height: 24px; font-size: 16px; border-top-width: 1px; border-top-color: #e2e8f0; border-top-style: solid; height: 1px; width: 100%; margin: 0;" align="left">

      </td>
    </tr>
  </tbody>
</table>
<table class="s-5 w-full" role="presentation" border="0" cellpadding="0" cellspacing="0" style="width: 100%;" width="100%">
  <tbody>
    <tr>
      <td style="line-height: 20px; font-size: 20px; width: 100%; height: 20px; margin: 0;" align="left" width="100%" height="20">
        &#160;
      </td>
    </tr>
  </tbody>
</table>

					<p style="line-height: 24px; font-size: 16px; width: 100%; margin: 0;" align="left">
						If you have any questions, please don't hesitate to <a href="{contact_us_link}" style="color: #0d6efd;">reach out</a>.
					</p>

      </td>
    </tr>
  </tbody>
</table>

      </td>
    </tr>
  </tbody>
</table>

      </td>
    </tr>
  </tbody>
</table>

      </td>
    </tr>
  </tbody>
</table>

      </td>
    </tr>
  </tbody>
</table></body>
</html>

'''


def signup_subject():
	return 'Welcome to SmorgasBoard!'

def signup_body_text():
	return f'''
Thanks for signing up for SmorgasBoard. We're excited to help make your next event unforgettable.

SmorgasBoard makes taking pictures more fun than ever before. You and your guests take pictures all over the event space and show them off on in an ever-evolving collage. The best part: at the end of the night, we'll send you all the pics.


Get started today!
1. Visit our website to create your board. Or, check out our free trial first to see SmorgasBoard in action.
2. On the day of your event, put your board up on a TV or projector, just as you would with a slideshow.
3. Your guests can easily tap a link or scan a QR code on their phones to add photos — no signup or app downloads required.


Contact us
If you have any questions, comments, or suggestions, we're all ears. To get in touch, just head to our contact page.
'''

def signup_body_html():
	return f'''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN" "http://www.w3.org/TR/REC-html40/loose.dtd">
<html>
<head>
    <!-- Compiled with Bootstrap Email version: 1.0.1 -->
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8">

          <style type="text/css">
            body,table,td{{font-family:Helvetica,Arial,sans-serif !important}}.ExternalClass{{width:100%}}.ExternalClass,.ExternalClass p,.ExternalClass span,.ExternalClass font,.ExternalClass td,.ExternalClass div{{line-height:150%}}a{{text-decoration:none}}*{{color:inherit}}a[x-apple-data-detectors],u+#body a,#MessageViewBody a{{color:inherit;text-decoration:none;font-size:inherit;font-family:inherit;font-weight:inherit;line-height:inherit}}img{{-ms-interpolation-mode:bicubic}}table:not([class^=s-]){{font-family:Helvetica,Arial,sans-serif;mso-table-lspace:0pt;mso-table-rspace:0pt;border-spacing:0px;border-collapse:collapse}}table:not([class^=s-]) td{{border-spacing:0px;border-collapse:collapse}}@media screen and (max-width: 600px){{.w-full,.w-full>tbody>tr>td{{width:100% !important}}.w-48,.w-48>tbody>tr>td{{width:192px !important}}.pt-2:not(table),.pt-2:not(.btn)>tbody>tr>td,.pt-2.btn td a,.py-2:not(table),.py-2:not(.btn)>tbody>tr>td,.py-2.btn td a{{padding-top:8px !important}}.pr-2:not(table),.pr-2:not(.btn)>tbody>tr>td,.pr-2.btn td a,.px-2:not(table),.px-2:not(.btn)>tbody>tr>td,.px-2.btn td a{{padding-right:8px !important}}.pb-2:not(table),.pb-2:not(.btn)>tbody>tr>td,.pb-2.btn td a,.py-2:not(table),.py-2:not(.btn)>tbody>tr>td,.py-2.btn td a{{padding-bottom:8px !important}}.pl-2:not(table),.pl-2:not(.btn)>tbody>tr>td,.pl-2.btn td a,.px-2:not(table),.px-2:not(.btn)>tbody>tr>td,.px-2.btn td a{{padding-left:8px !important}}.pr-4:not(table),.pr-4:not(.btn)>tbody>tr>td,.pr-4.btn td a,.px-4:not(table),.px-4:not(.btn)>tbody>tr>td,.px-4.btn td a{{padding-right:16px !important}}.pl-4:not(table),.pl-4:not(.btn)>tbody>tr>td,.pl-4.btn td a,.px-4:not(table),.px-4:not(.btn)>tbody>tr>td,.px-4.btn td a{{padding-left:16px !important}}*[class*=s-lg-]>tbody>tr>td{{font-size:0 !important;line-height:0 !important;height:0 !important}}.s-2>tbody>tr>td{{font-size:8px !important;line-height:8px !important;height:8px !important}}}}

          </style>
</head>
<body class="bg-dark" style="outline: 0; width: 100%; min-width: 100%; height: 100%; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; font-family: Helvetica, Arial, sans-serif; line-height: 24px; font-weight: normal; font-size: 16px; -moz-box-sizing: border-box; -webkit-box-sizing: border-box; box-sizing: border-box; color: #000000; margin: 0; padding: 0; border: 0;" bgcolor="#1a202c"><table class="bg-dark body" valign="top" role="presentation" border="0" cellpadding="0" cellspacing="0" style="outline: 0; width: 100%; min-width: 100%; height: 100%; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%; font-family: Helvetica, Arial, sans-serif; line-height: 24px; font-weight: normal; font-size: 16px; -moz-box-sizing: border-box; -webkit-box-sizing: border-box; box-sizing: border-box; color: #000000; margin: 0; padding: 0; border: 0;" bgcolor="#1a202c">
  <tbody>
    <tr>
      <td valign="top" style="line-height: 24px; font-size: 16px; margin: 0;" align="left" bgcolor="#1a202c">

	<table class="px-4 bg-dark w-full" role="presentation" border="0" cellpadding="0" cellspacing="0" style="width: 100%;" bgcolor="#1a202c" width="100%">
  <tbody>
    <tr>
      <td style="line-height: 24px; font-size: 16px; width: 100%; padding-right: 16px; padding-left: 16px; margin: 0;" align="left" bgcolor="#1a202c" width="100%">

		<a href="{homepage_link}" style="color: #0d6efd;">
			<table class="ax-center" role="presentation" align="center" border="0" cellpadding="0" cellspacing="0" style="margin: 0 auto;">
  <tbody>
    <tr>
      <td style="line-height: 24px; font-size: 16px; margin: 0;" align="left">
        <img class="w-48" style="height: auto; line-height: 100%; outline: none; text-decoration: none; display: block; width: 192px; padding: 4px; border: 0 none;" src="https://smorgasboard.io/assets/logo-color.png" width="192">
      </td>
    </tr>
  </tbody>
</table>
		</a>
		<table class="py-2 bg-dark border-0 rounded-md w-full" role="presentation" border="0" cellpadding="0" cellspacing="0" style="border-radius: 6px; width: 100%; border: 0px solid #e2e8f0;" bgcolor="#1a202c" width="100%">
  <tbody>
    <tr>
      <td style="line-height: 24px; font-size: 16px; border-radius: 6px; width: 100%; padding-top: 8px; padding-bottom: 8px; margin: 0;" align="left" bgcolor="#1a202c" width="100%">

			<table class="card" role="presentation" border="0" cellpadding="0" cellspacing="0" style="border-radius: 6px; border-collapse: separate !important; width: 100%; overflow: hidden; border: 1px solid #e2e8f0;" bgcolor="#e1e1e1">
  <tbody>
    <tr>
      <td style="line-height: 24px; font-size: 16px; width: 100%; margin: 0;" align="left" bgcolor="#ffffff">

				<table class="card-body" role="presentation" border="0" cellpadding="0" cellspacing="0" style="width: 100%;">
  <tbody>
    <tr>
      <td style="line-height: 24px; font-size: 16px; width: 100%; margin: 0; padding: 20px;" align="left">

					<table class="px-2" role="presentation" border="0" cellpadding="0" cellspacing="0">
  <tbody>
    <tr>
      <td style="line-height: 24px; font-size: 16px; padding-right: 8px; padding-left: 8px; margin: 0;" align="left">
        <div class="">
						<p class="text-xl text-gray-600" style="line-height: 24px; font-size: 20px; color: #718096; width: 100%; margin: 0;" align="left">
							Thanks for signing up for SmorgasBoard. We're excited to help make your next event unforgettable.
						</p>
						<br>
						<p style="line-height: 24px; font-size: 16px; width: 100%; margin: 0;" align="left">
							SmorgasBoard makes taking pictures more fun than ever before. You and your guests take pictures all over the event space and show them off on in an ever-evolving collage. The best part: at the end of the night, we'll send you all the pics.
						</p>
					</div>
      </td>
    </tr>
  </tbody>
</table>

					<div class="hr-partial" style="border-top-width: 1px; border-top-color: grey; border-top-style: solid; margin: 20px 10px;"></div>

					<div>
						<p class="text-xl" style="line-height: 24px; font-size: 20px; width: 100%; margin: 0;" align="left">
							Get started today!
						</p>
						<ol>
							<li style="margin-left: -1rem;">
								Visit our website to <a href="{get_started_link}" style="color: #0d6efd;">create your board</a>. Or, check out our <a href="{free_trial_link}" style="color: #0d6efd;">create your board</a> first to see SmorgasBoard in action.
							</li>
							<li style="margin-left: -1rem;">
								On the day of your event, put <a href="{all_boards_link}" style="color: #0d6efd;">your board</a> up on a TV or projector, just as you would with a slideshow.
							</li>
							<li style="margin-left: -1rem;">
								Your guests can easily tap a link or scan a QR code on their phones to add photos &#8212; no signup or app downloads required.
							</li>
						</ol>
					</div>

					<div class="hr-partial" style="border-top-width: 1px; border-top-color: grey; border-top-style: solid; margin: 20px 10px;"></div>

					<div>
						<p class="text-xl" style="line-height: 24px; font-size: 20px; width: 100%; margin: 0;" align="left">
							Contact us
						</p>
						<table class="s-2 w-full" role="presentation" border="0" cellpadding="0" cellspacing="0" style="width: 100%;" width="100%">
  <tbody>
    <tr>
      <td style="line-height: 8px; font-size: 8px; width: 100%; height: 8px; margin: 0;" align="left" width="100%" height="8">
        &#160;
      </td>
    </tr>
  </tbody>
</table>
<p class="" style="line-height: 24px; font-size: 16px; width: 100%; margin: 0;" align="left">
							If you have any questions, comments, or suggestions, we're all ears. To get in touch, just head to our <a href="{contact_us_link}" style="color: #0d6efd;">contact page</a>.
						</p>
					</div>

      </td>
    </tr>
  </tbody>
</table>

      </td>
    </tr>
  </tbody>
</table>

      </td>
    </tr>
  </tbody>
</table>

      </td>
    </tr>
  </tbody>
</table>

      </td>
    </tr>
  </tbody>
</table></body>
</html>
'''



