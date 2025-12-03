from flask import jsonify, request, Response
import yappi
import time
from functools import wraps
import json

def profile_request(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            print('execute wrapper')
            yappi.clear_stats()
            yappi.set_clock_type("wall")
            yappi.start()
            result = func(*args, **kwargs)
            yappi.stop()
            return result
        return wrapper

def init_myappi(app):

    @app.get("/yappi-stats")
    def yappi_stats():
        yappi.get_func_stats().sort("ttot", "desc")

        stats = []
        for s in yappi.get_func_stats():
            stats.append({
                "name": s.name,
                "module": s.module,
                "lineno": s.lineno,
                "ncall": s.ncall,
                "t_total_cpu": round(s.ttot, 6),  # total time
                "t_sub_cpu": round(s.tsub, 6),    # time excluding subcalls
                "t_avg_cpu": round(s.tavg, 6)     # avg call time
            })
        t = int(time.time())
        ystat = yappi.get_func_stats()
        ystat.save(f"profile_{t}.callgrind", type="callgrind")
        ystat.save(f"profile_{t}.pstat", type="pstat")
        return jsonify(stats)
    
    @app.before_request
    def yappi_before():
        if request.headers.get("X-Profile") == "1":
            yappi.clear_stats()
            yappi.set_clock_type("wall")
            yappi.start()
            request._profiling = True
        else:
            request._profiling = False

    @app.after_request
    def yappi_after(response: Response):
        if request._profiling:
            yappi.stop()
            stats = yappi.get_func_stats()
            stats.sort("ttot", "desc")

            # zapis plików
            # t = int(time.time())
            # stats.save(f"profile_{t}.callgrind", type="callgrind")
            # stats.save(f"profile_{t}.pstat", type="pstat")

            # wrzucamy staty do response JSON — tylko jeśli response jest JSONem
            try:
                data = response.get_json()
                data["_profile"] = [{
                    "name": s.name,
                    "module": s.module,
                    "lineno": s.lineno,
                    "ncall": s.ncall,
                    "t_total_cpu": round(s.ttot, 6),
                    "t_sub_cpu": round(s.tsub, 6),
                    "t_avg_cpu": round(s.tavg, 6)
                } for s in stats[:20]]  # TOP 20

                # response.set_data(jsonify(data).data)
                response.headers['X-yappi'] = json.dumps(data["_profile"])
            except Exception:
                pass

        return response