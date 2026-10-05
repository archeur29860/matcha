from flask import jsonify


def success(data=None, status=200):
    '''
    Return normalisé de code succès
    '''
    return jsonify({
        "success": True,
        "data": data,
        "error": None
    }), status


def error(code, message, status=400, details=None):
    '''
    Return normalisé de code erreur
    '''
    return jsonify({
        "success": False,
        "data": None,
        "error": {
            "code": code,
            "message": message,
            "details": details
        }
    }), status