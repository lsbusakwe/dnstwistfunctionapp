import logging
import azure.functions as func
import subprocess

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function received a request.')

    try:
        # Extract route parameters if using custom routes (e.g., /trigger/{domain}/{output_type})
        domain = req.route_params.get('domain')
        output_type = req.route_params.get('output_type')

        # If route parameters are not provided, check the request body for parameters
        if not domain or not output_type:
            try:
                req_body = req.get_json()
                domain = req_body.get('domain')
                output_type = req_body.get('output_type')
            except ValueError:
                return func.HttpResponse("Invalid request body", status_code=400)
        
        # Check if both parameters are available
        if not domain or not output_type:
            return func.HttpResponse("Please provide both 'domain' and 'output_type'.", status_code=400)

        # Log the extracted parameters
        logging.info(f"domain: {domain}, output_type: {output_type}")

        # Example: Prepare the command-line arguments to pass to your script
        command = ['python3', 'dnstwist/dnstwist.py', '-r -w -f', output_type,  domain]

        # Execute the command using subprocess and capture the output
        result = subprocess.run(command, capture_output=True, text=True)

        # Return the output from the subprocess call in the HTTP response
        if result.returncode == 0:
            return func.HttpResponse(f"Script executed successfully: {result.stdout}", status_code=200)
        else:
            return func.HttpResponse(f"Script execution failed: {result.stderr}", status_code=500)

    except Exception as e:
        logging.error(f"Error occurred: {str(e)}")
        return func.HttpResponse(f"Error: {str(e)}", status_code=500)

