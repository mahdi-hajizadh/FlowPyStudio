import sys
import io
from contextlib import redirect_stdout
import subprocess
import tempfile
import os

class CodeRunner:
    def __init__(self):
        self.output = None
        self.error = None
        
    def run(self, code):
        """Execute Python code and capture output"""
        if not code or not code.strip():
            return "No code to execute"
            
        output_buffer = io.StringIO()
        try:
            with redirect_stdout(output_buffer):
                exec(code, {})
        except (Exception, SystemExit) as error:
            return f"Error: {error}"

        return output_buffer.getvalue() or "Code executed successfully (no output)"

    def run_with_subprocess(self, code):
        """Execute code in a subprocess with a timeout"""
        if not code or not code.strip():
            return "No code to execute"
            
        try:
            # Write code to temporary file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
                
            # Run the script
            result = subprocess.run(
                [sys.executable, temp_file],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            # Clean up
            os.unlink(temp_file)
            
            output = result.stdout
            if result.stderr:
                output += "\n" + result.stderr
                
            return output if output else "Code executed successfully (no output)"
            
        except subprocess.TimeoutExpired:
            return "Error: Code execution timed out (30 seconds)"
        except Exception as e:
            return f"Error: {str(e)}"
