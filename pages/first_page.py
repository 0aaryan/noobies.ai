import streamlit as st
from clarifai.client.auth import create_stub
from clarifai.client.auth.helper import ClarifaiAuthHelper
from clarifai.client.user import User
from clarifai.modules.css import ClarifaiStreamlitCSS
from google.protobuf import json_format, timestamp_pb2

st.set_page_config(layout="wide")
ClarifaiStreamlitCSS.insert_default_css(st)

# This must be within the display() function.
auth = ClarifaiAuthHelper.from_streamlit(st)
stub = create_stub(auth)
userDataObject = auth.get_user_app_id_proto()

st.title("Simple example to list inputs")

with st.form(key="data-inputs"):
  mtotal = st.number_input(
      "Select number of inputs to view in a table:", min_value=5, max_value=100)
  submitted = st.form_submit_button('Submit')

if submitted:
  if mtotal is None or mtotal == 0:
    st.warning("Number of inputs must be provided.")
    st.stop()
  else:
    st.write("Number of inputs in table will be: {}".format(mtotal))

  # Stream inputs from the app. list_inputs give list of dictionaries with inputs and its metadata .
  input_obj = User(user_id=userDataObject.user_id).app(app_id=userDataObject.app_id).inputs()
  all_inputs = input_obj.list_inputs()

  #Check for no of inputs in the app and compare it with no of inputs to be displayed.
  if len(all_inputs) < (mtotal):
    raise Exception(
        f"No of inputs is less than {mtotal}. Please add more inputs or reduce the inputs to be displayed !"
    )

  else:
    data = []
    #added "data_url" which gives the url of the input.
    for inp in range(mtotal):
      data.append({
          "id": all_inputs[inp].id,
          "data_url": all_inputs[inp].data.image.url,
          "status": all_inputs[inp].status.description,
          "created_at": timestamp_pb2.Timestamp.ToDatetime(all_inputs[inp].created_at),
          "modified_at": timestamp_pb2.Timestamp.ToDatetime(all_inputs[inp].modified_at),
          "metadata": json_format.MessageToDict(all_inputs[inp].data.metadata),
      })

  st.dataframe(data)
