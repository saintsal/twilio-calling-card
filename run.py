# This little script does two things:
# If you call it, it allows you to dial an outbound number, so you pay Twilio's cheap long distance rates
# If someone else calls it, it'll forward the call to your numbers.

from flask import Flask, request, redirect
import twilio.twiml

app = Flask(__name__)

# Add your numbers here.  The script will only allow outbound calls if it identifies one of these numbers is calling.

callers = {
    "+4420800000",
    "+35988912345"
}



@app.route("/", methods=['GET', 'POST'])
def hello_monkey():
    from_number = request.values.get('From', None)
    resp = twilio.twiml.Response()

    if from_number in callers:
# Greet the caller by name
        resp.say("Hello Sal.")
# Say a command, and listen for the caller to press a key. When they press
# a key, redirect them to /handle-key.
        with resp.gather(action="/handle-key", method="POST") as g:
            g.say("Go for it!")

    else:
        # Add your numbers here. It'll try them in order
        resp.dial("+16045555555")
        resp.dial("+1447777888888")


    return str(resp)



@app.route("/handle-key", methods=['GET', 'POST'])
def handle_key():
# Get the digit pressed by the user. They should probably end with #
    digit_pressed = request.values.get('Digits', None)
    resp = twilio.twiml.Response()
# Dial the number that was typed
        resp.dial(digit_pressed)

    resp.say("Sorry, the call failed. Goodbye.")
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
