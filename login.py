import dash 
from dash import html, dcc
from dash.dependencies import Output,Input,State
# from mysql.connector import connect, Error
import dash_bootstrap_components as dbc
import pandas as pd
import mysql.connector
import re

mydb = mysql.connector.connect(
    
    host = "localhost",
    database = "web-app",
    user = "root",
    password = "root",

)

query = "SELECT userId, first_name, last_name, city, country, password FROM users WHERE email_id = %s and password = %s"
is_email_exist_query = "SELECT email_id FROM users WHERE email_id = %s "
insert_query = "insert into users (full_name, email_id, password) VALUES( %s, %s, %s ) "
email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'


container_class = "container"

# app = dash.Dash(__name__, external_stylesheets=external_stylesheets,suppress_callback_exceptions=True)
external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, suppress_callback_exceptions=True)

app.layout = html.Div([
  dcc.Location(id='url', refresh=False),
  html.Div(id='page-content')
                     ])

#index page
index_page = html.Div(
    className="container",
    id="container",
    children=[
    
        #Sign Up Container
        html.Div(
            className="form-container sign-up-container",
            children=[
                html.Div(
                    className = "form-css",
                    children = [
                        html.H1('Create Account'),
                        html.Div(
                        className="social-container",
                        children= [ 
                                
                                html.A(html.I(className="fab fa-facebook-f"),
                                    href="#",
                                    className="social",
                                ),
                                html.A(html.I(className="fab fa-google-plus-g"),
                                    href="#",
                                    className="social",
                                ),
                                html.A(html.I(className="fab fa-linkedin-in"),
                                    href="#",
                                    className="social",
                                ),
                            
                            ]
                        ),

                        html.Span('or use your email for registration'),
                        dcc.Input(id="full_name", type="text", placeholder = "Name"),
                        dcc.Input(id="email_sup", type="email", placeholder = "Email"),
                        dcc.Input(id="passw_sup", type="password", placeholder = "Password"),
                        html.Div(id='output2'),
                        html.Button('SIGN UP', id='verify_sup'),
                        
                    ],
                    
                )                
            ]
        ),
        #sign In Container
        
        html.Div(
            className="form-container sign-in-container",
            children=[
                html.Div(
                    className = "form-css",
                    children = [
                        html.H1('Sign In'),
                        html.Div(
                        className="social-container",
                        children= [ 
                                
                                html.A(html.I(className="fab fa-facebook-f"),
                                    href="#",
                                    className="social",
                                ),
                                html.A(html.I(className="fab fa-google-plus-g"),
                                    href="#",
                                    className="social",
                                ),
                                html.A(html.I(className="fab fa-linkedin-in"),
                                    href="#",
                                    className="social",
                                ),
                            
                            ]
                        ),

                        
                        html.Span('or use your account'),
                        dcc.Input(id="email_sin", type="email", placeholder = "Email"),
                        dcc.Input(id="passw_sin", type="password", placeholder = "Password"),
                        html.Div(id='output1'),
                        html.A('Forgot your password?', href="#", ),
                        html.Button('SIGN IN', id='verify'),
                        
                    ],
                    
                )                
            ]
        ),
        html.Div(
            className="overlay-container",
            children=html.Div(
                className="overlay",
                children=[
                    html.Div(
                        className="overlay-panel overlay-left",
                        children=[
                            html.H1('Welcome Back!'),
                            html.P('To keep connected with us please login with your personal info'),
                            html.Button('SIGN IN', id='signIn',  className="ghost"),
                        ]

                    ),
                    html.Div(
                        className="overlay-panel overlay-right",
                        children=[
                            html.H1('Hello, Friend!'),
                            html.P('Enter your personal details and start journey with us'),
                            html.Button('SIGN UP', id='signUp',  className="ghost"),
                        ]

                    )
                ]
            ),
        )

    ]
)

# index_page = html.Div(
#     className="log-form",
#         children=[
#             dcc.Input(id="user", type="text", placeholder = "Enter Username"),
#             dcc.Input(id="passw", type="password", placeholder = "Enter Password"),
#             html.Button('Login', id='verify', n_clicks=0, className = "btn"),
#             html.A('Forgot Password?', href='#', className="forgot"),
#             html.Div(id='output1')
#         ]
# )



@app.callback(
dash.dependencies.Output('output1', 'children'),
   [dash.dependencies.Input('verify', 'n_clicks')],
    [State('email_sin', 'value'),State('passw_sin', 'value')]
    )
def update_output(n_clicks, uname, passw):
    li={'admin':'admin'}
    if uname != '' and uname != None and passw != '' and passw != None :
        
        mydb._open_connection()
        cursor = mydb.cursor()
        cursor.execute(query, (uname, passw ))
        usersSet = cursor.fetchall()

        mydb.commit()
        cursor.close()
        mydb.close()

    if (uname =='' or uname == None) and (passw =='' or passw == None):
        return html.Div(children='')
    if uname == '' or uname == None:
        return html.Div(children='Invalid Username',className="error-messages")
    if passw == '' or passw == None:
        return html.Div(children='Invalid Password',className="error-messages")
    if usersSet == [] or len(usersSet) == 0:
        return html.Div(children='Invalid Username or Password',className="error-messages")
    if (usersSet != [] and len(usersSet) > 0):
        # return html.Div(dcc.Link('Access Granted!', href='/next_page',style={'color':'#183d22','font-family': 'serif', 'font-weight': 'bold', "text-decoration": "none",'font-size':'20px'}),style={'padding-left':'605px','padding-top':'40px'})
        return html.Div(children='Logged In Successfully!',className="success-messages")
    else:
        return html.Div(children='Invalid Password',className="error-messages")


#On Sign-Up
    
    
@app.callback(
dash.dependencies.Output('output2', 'children'),
   [dash.dependencies.Input('verify_sup', 'n_clicks')],
    [State('email_sup', 'value'),State('passw_sup', 'value'),State('full_name', 'value')]
    )
def update_output(n_clicks, email, passw, full_name):
    emailData = []
    print("================================Inside SignUp================================",is_email_exist_query)
    if (email != '' and email != None and re.fullmatch(email_regex, email))and passw != '' and passw != None and full_name != '' and full_name != None :
        
        mydb._open_connection()
        cursor = mydb.cursor()
        # print("is_email_exist_query=============>>>>",is_email_exist_query)
        value = [email]
        cursor.execute(is_email_exist_query, value)
        emailData = cursor.fetchall()

        mydb.commit()
        cursor.close()
        mydb.close()

    if (email =='' or email == None) and (passw =='' or passw == None) and (full_name =='' or full_name == None):
        return html.Div(children='')
    if full_name == '' or full_name == None:
        return html.Div(children='Invalid Name!',className="error-messages")
    if email == '' or email == None or re.fullmatch(email_regex, email) == None:
        return html.Div(children='Invalid Email Id',className="error-messages")
    if passw == '' or passw == None:
        return html.Div(children='Invalid Password',className="error-messages")
    if (emailData != [] and len(emailData) > 0):
        return html.Div(children='Email Already Exists!',className="error-messages")    
    if (emailData == [] and len(emailData) == 0):
        mydb._open_connection()
        cursor = mydb.cursor()
        cursor.execute(insert_query, (full_name, email, passw ))

        mydb.commit()
        cursor.close()
        mydb.close()

        
        return html.Div(children='Account created successfully. Please Sign In.',className="success-messages")
    
    else:
        return html.Div(children='Invalid Details!',className="error-messages")



next_page = html.Div([
    html.Div(dcc.Link('Log out', href='/',style={'color':'#bed4c4','font-family': 'serif', 'font-weight': 'bold', "text-decoration": "none",'font-size':'20px'}),style={'padding-left':'80%','padding-top':'10px'}),
    html.H1(children="This is the Next Page, the main Page",className="ap",style={
        'color':'#89b394','text-align':'center','justify':'center','padding-top':'170px','font-weight':'bold',
        'font-family':'courier',
        'padding-left':'1px'  })
    ]) 


@app.callback(dash.dependencies.Output('page-content', 'children'),[dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/next_page':
        return next_page
    else:
       return index_page


#Toggling Sign In| Sign Up Container
@app.callback(
    Output("container", "className"),
    Input('signUp', 'n_clicks'),
    Input('signIn', 'n_clicks'),
    [State("container", "className")],
    prevent_initial_call=True,
)
def callback(n_clicks, btn, current_classes):
    if "right-panel-active" in current_classes:
        return container_class
    return container_class + " right-panel-active"
        

if __name__=='__main__':
    app.run_server() 
