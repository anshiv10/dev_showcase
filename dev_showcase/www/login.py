import frappe
from frappe import _

no_cache = 1


def _safe_path(path):
	"""Allow only same-site paths like /app/sales-order, never //evil.com."""
	if path and path.startswith("/") and not path.startswith("//") and not path.startswith("/\\"):
		return path
	return None


def get_context(context):
	redirect_to = _safe_path(frappe.form_dict.get("redirect-to"))

	# Already logged in? Skip the login page.
	if frappe.session.user != "Guest":
		frappe.local.flags.redirect_location = redirect_to or "/app"
		raise frappe.Redirect

	context.no_header = 1
	context.no_breadcrumbs = 1
	context.title = _("Login")
	context.site = frappe.local.site
	context.redirect_to = redirect_to or ""
	return context