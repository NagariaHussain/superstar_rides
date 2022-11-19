import frappe

no_cache = 1


def get_context(context):
    context.secret_message = "Something cool"
    return context
