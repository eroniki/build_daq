from flask import redirect, request, url_for

# Redirect to the endpoint in the next parameter...
# if it exists and is valid, else redirect to a fallback
def redirect_dest(fallback):
	dest = request.args.get('next')
	try:
		dest_url = url_for(dest)
	except:
		return redirect(fallback)
	return redirect(dest_url)
