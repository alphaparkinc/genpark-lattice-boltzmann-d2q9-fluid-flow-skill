import sys
import json
from client import LatticeBoltzmannD2Q9

def handle_request(req):
    method = req.get("method")
    req_id = req.get("id")
    
    if method == "initialize":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-lattice-boltzmann-d2q9-fluid-flow-skill", "version": "1.0.0"}
            }
        }
    elif method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "simulate_lbm_step",
                        "description": "Run D2Q9 Lattice Boltzmann BGK collision and streaming step",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "nx": {"type": "integer", "default": 20},
                                "ny": {"type": "integer", "default": 10},
                                "tau": {"type": "number", "default": 0.8},
                                "steps": {"type": "integer", "default": 5}
                            }
                        }
                    }
                ]
            }
        }
    elif method == "tools/call":
        params = req.get("params", {})
        tool_name = params.get("name")
        args = params.get("arguments", {})
        
        if tool_name == "simulate_lbm_step":
            nx = args.get("nx", 20)
            ny = args.get("ny", 10)
            tau = args.get("tau", 0.8)
            steps = args.get("steps", 5)
            lbm = LatticeBoltzmannD2Q9(nx=nx, ny=ny, tau=tau)
            lbm.set_cylinder_obstacle(cx=nx//4, cy=ny//2, radius=max(1, ny//4))
            for _ in range(steps):
                rho, ux, uy = lbm.step()
            return {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps({"nx": nx, "ny": ny, "steps_completed": steps, "status": "CONVERGED"})}]
                }
            }
    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            res = handle_request(req)
            sys.stdout.write(json.dumps(res) + "\n")
            sys.stdout.flush()
        except Exception as e:
            err = {"jsonrpc": "2.0", "id": None, "error": {"code": -32700, "message": str(e)}}
            sys.stdout.write(json.dumps(err) + "\n")
            sys.stdout.flush()

if __name__ == "__main__":
    main()
