# Mobile simulation & server

enviornment setup:

1. server
   install flask

   ```cd server
   export FLASK_APP=flaskr
   export FLASK_ENV=development
   export MONGO_URI=<your uri>
   flask run
   ```

2. mobiles<br>
   adjust parameters when creating env (in `main.py`)
   <br>
   change parameters in `constant.py ` if needed
   <br>
   start by `python main.py`

3. /testdata/ <br>
   `patient.npy` in `/testdata/` can be used as the patient's embedding
