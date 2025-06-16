from flask import Blueprint, jsonify
import psutil

bp = Blueprint('performance', __name__)

@bp.route('/system', methods=['GET'])
def get_system_performance():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()
    
    return jsonify({
        'cpu_percent': cpu_percent,
        'memory_percent': memory_info.percent,
        'memory_total_gb': round(memory_info.total / (1024**3), 2),
        'memory_used_gb': round(memory_info.used / (1024**3), 2)
    }) 