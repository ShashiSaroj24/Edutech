from django.shortcuts import render,redirect
from EduApp.models import *
import random
from django.conf import settings
from django.core.mail import send_mail
import pandas as pd 
import plotly.express as px
import plotly.graph_objects as go 
import itertools
import statsmodels.api as sm
from django.shortcuts import render
import joblib
import numpy as np
import joblib
import pickle
from django.http import HttpResponse
from datetime import datetime, timedelta
from newsapi import NewsApiClient
from django.conf import settings


# Create your views here.
def Home(request):
	return render(request,'Index.html')

def AboutUs(request):
	return render(request,'AboutUs.html')

def Dashboard(request):
	if not request.session.has_key('em'):
		return redirect('/Login')
	user=Register_model.objects.get(Email=request.session['em'])
	if request.method=="POST":
		print("yes")
		user.ProfileImg=request.FILES['fs']
		user.save()
		print("done")
		return render(request,'Dashboard.html',{'user':user,'msg':'Success'})
	else:
		return render(request,'Dashboard.html',{'user':user})

def Register(request):
	if request.method=="POST":
			n=request.POST.get('nm')
			e=request.POST.get('em')
			p=request.POST.get('pw')
			cp=request.POST.get('cpw')
			if p == cp:
				if Register_model.objects.filter(Email=e).exists():
					return render(request,'Register.html',{'Error':"Email Id is Already Exists"})
				else:
					OTP=random.randrange(100000,999999)
					subject="OTP"
					message="Welcome! Your OTP is" +str(OTP)
					email_from=settings.EMAIL_HOST_USER
					recipient_list=[e]
					send_mail(subject,message,email_from,recipient_list)
					message="Your OTP sent to your respective Email Account"
					print("Enter page otp")
					return render(request,'Register1.html',{'Name':n,'Email':e, 'Password':p, 'Org_OTP':OTP,'msg':message})
			else:
				print("else part pass & c-pass")
				return render(request,'Register.html',{'Error':"Password and Confirm Password Does Not Match"})
	else:
		return render(request,'Register.html')

def Check_OTP(request):
	if request.method=="POST":
		n=request.POST.get('nm')
		e=request.POST.get('em')
		p=request.POST.get('pw')
		Org=request.POST.get("Org_OTP")
		Enter=request.POST.get('Enter_OTP')
		if Org==Enter:
			x=Register_model()
			x.Name=n
			x.Email=e
			x.Password=p
			x.save()
			return render(request,"Thankyou.html")
		else:
			return render(request,"Register1.html",{'Name':n, 'Email':e, 'Password':p,'Org_OTP':Org})


def Login(request):
	if request.method=="POST":
		e=request.POST.get('em')
		p=request.POST.get('pw')
		user=Register_model.objects.filter(Email=e, Password=p)
		if len(user)>0:
			request.session['em']=e
			return redirect("/Dashboard")
		else:
			return render(request,"login.html",{"msg":"User does not Exist"})
	return render(request,'Login.html')

def Contact(request):
		if request.method=="POST":
			x=Contact_model()
			x.Name=request.POST.get('nm')
			x.Email=request.POST.get('em')
			x.msg=request.POST.get('pw')
			x.save()
			return render(request,'Contact.html',{'msg':"Success"})
		else:
			return render(request,'Contact.html')


def ForgetPassword(request):
	if (request.method=='POST'):
		e=request.POST.get('em')
		user=Register_model.objects.filter(Email=e)
		if(len(user)>0):
			pw=user[0].Password
			subject="Password"
			message="Welcome! Your Password is" + str(pw)
			email_from=settings.EMAIL_HOST_USER
			recipient_list=[e]
			send_mail(subject,message,email_from,recipient_list)
			res="Your Password sent to your respective Email Account"
			return render(request,'Forget Password.html',{'msg':res})
		else:
			rest='This Email Id is Not Registered'
			return render(request,'Forget Password.html',{'Error':rest})
	else:
		return render(request,'Forget Password.html')

def Email(request):
    if request.method == 'POST':
        e = request.POST.get('em')
        if e:
	            email_from = settings.EMAIL_HOST_USER
	            recipient_list = [e]
	            subject = "Registration Successful"
	            message = "Thank you for registering."
	            send_mail(subject, message, email_from, recipient_list)
	            return render(request, 'Success.html')
        else:
            return render(request, 'Success.html')


def Base(request):
	return render(request,'Base.html')

def UserProfile(request):
	if not request.session.has_key('em'):
		return redirect('/Login')
	user=Register_model.objects.get(Email=request.session['em'])
	if request.method=="POST":
		print("yes")
		user.ProfileImg=request.FILES['fs']
		user.save()
		print("done")
		return render(request,'User Profile.html',{'user':user,'msg':'Success'})
	else:
		return render(request,'User Profile.html',{'user':user})
	
def Sidebar(request):
	return render(request,'Sidebar.html')

def Thankyou(request):
	return render(request,'Thankyou.html')

def HelpAndSupport(request):
	if not request.session.has_key('em'):
		return redirect('/Login')
	user=Register_model.objects.get(Email=request.session['em'])
	if request.method=="POST":
		X=HelpandSupport()
		X.Title=request.POST.get('ti')
		X.Message=request.POST.get('msg')
		X.save()
		res="Data Successfully Added"
		return render(request,'HelpAndSupport.html',{'res':res,'user':user})
	else:
		Error="Data Not Added Successfully"
		return render(request,'HelpAndSupport.html',{'Error':Error,'user':user})


def ChangePassword(request):
	if not request.session.has_key('em'):
		return redirect('/Login')
	user=Register_model.objects.get(Email=request.session['em'])
	if request.method=='POST':
		re=Register_model.objects.get(Email=request.session['em'])
		op=request.POST.get('opw')
		np=request.POST.get('npw')
		cp=request.POST.get('cpw')

		if (np==cp):
			pa=re.Password
			if(op==pa):
				re.Password=np
				re.save()
				res="Password Changed"
				return render(request,'Change Password.html',{'res':res})
			else:
				Error="Invalid Current Password"
				return render(request,'Change Password.html',{'Error':Error})
		else:
			Error="Confirm Password and New Password Does Not Match"
			return render(request,'Change Password.html',{'Error':Error})
	else:
		return render(request,'Change Password.html',{'user':user})

def EditProfile(request):
	if not request.session.has_key('em'):
		return redirect('/Login')
	user=Register_model.objects.get(Email=request.session['em'])
	if request.method=="POST":
		user.Name=request.POST.get('nm')
		user.Pincode=request.POST.get('pc')
		user.PhoneNo=request.POST.get('pn')
		user.DOB=request.POST.get('dob')
		user.City=request.POST.get('city')
		user.Address=request.POST.get('add')
		user.ProfileImg=request.FILES['fs']
		user.save()
		return redirect('/UserProfile')
	else:
		return render(request,'Edit Profile.html',{'user':user})

def LatestNews(request):
    newsapi = NewsApiClient(api_key='74c605ea00cd4d7a8a3e779dd098702d')

    # Fetch articles from the past 29 days
    json_data = newsapi.get_everything(
        q='Education',
        language='en',
        from_param=(datetime.today() - timedelta(days=29)).strftime('%Y-%m-%d'),
        to=datetime.today().strftime('%Y-%m-%d'),
        page_size=24,
        page=2,
        sort_by='relevancy'
    )

    articles = json_data['articles']
    print("art====",articles)
    return render(request, 'LatestNews.html', {'k': articles})

def Logout(request):
	if not request.session.has_key('em'):
		return redirect('/Login')
	del request.session['em']
	return redirect('/Login')
	return render(request,'Sidebar.html')

def Articles(request):
	x=Article.objects.all()
	return render(request,'Articles.html',{'data':x})

def Laws(request):
	x=law.objects.all()
	return render(request,'Laws.html',{'data':x})

def Laws_Details(request,id):
	data=law.objects.get(id=id)
	return render(request,'Laws_Details.html',{'i':data})

def Colleges(request):
	x=College.objects.all()
	return render(request,'Colleges.html',{'data':x})

def University(request):
	x=Universitie.objects.all()
	return render(request,'University.html',{'data':x})

def View_Articles(request,id):
	data=Article.objects.get(id=id)
	return render(request,'View_Article.html',{'data':data})

def Courses(request):
	user=Register_model.objects.get(Email=request.session['em'])
	x=Course.objects.all()
	return render(request,'Courses.html',{'data':x,'user':user})

def Exams(request, name):
	user=Register_model.objects.get(Email=request.session['em'])
	x=Exam.objects.filter(Name=name)
	return render(request,'Exams.html',{'data':x,'name':name,'user':user},)

def Coordinators(request):
	x=EduInst.objects.all()
	return render(request,'Coordinators.html',{'Data':x})

def Coordinators_Details(request,Name):
	x=EduInst.objects.get(Name=Name)
	return render(request,'Coordinators Details.html',{'Data':x})

def Statistics(request):
	user=Register_model.objects.get(Email=request.session['em'])
	if request.method=="POST":
		x=statistic.objects.all()
		res=request.POST.get('se')
		print(res)
		y=statistic_detail.objects.filter(Statistic=res)
		return render(request,'Statistics.html',{'data':x, 'search_data':y, 'res':res, 'user':user})
	else:
		x=statistic.objects.all()
		print("else part")
		return render(request,'Statistics.html',{'data':x,'user':user})

def States(request):
	user=Register_model.objects.get(Email=request.session['em'])
	x=State_and_Universitie.objects.all()
	return render(request,'States.html',{'data':x,'user':user})

def Analytics(request):
	user=Register_model.objects.get(Email=request.session['em'])
	return render(request,'Analytics.html',{'user':user})

def State_University_Details(request, name):
	user=Register_model.objects.get(Email=request.session['em'])
	x=Universities_detail.objects.filter(State_Name=name)
	return render(request,'Statewise_Universities.html',{'data':x, 'name':name,'user':user})

def EduAnalysis1(request):
	user=Register_model.objects.get(Email=request.session['em'])
	return render(request,'EduAnalysis1.html',{'user':user})

def EduAnalysis2(request):
	user=Register_model.objects.get(Email=request.session['em'])
	return render(request,'EduAnalysis2.html',{'user':user})

def EduAnalysis3(request):
	user=Register_model.objects.get(Email=request.session['em'])
	return render(request,'EduAnalysis3.html',{'user':user})

def EduAnalysis4(request):
	user=Register_model.objects.get(Email=request.session['em'])
	return render(request,'EduAnalysis4.html',{'user':user})

def EduAnalysis5(request):
	user=Register_model.objects.get(Email=request.session['em'])
	return render(request,'EduAnalysis5.html',{'user':user})

def EduAnalysis6(request):
	user=Register_model.objects.get(Email=request.session['em'])
	return render(request,'EduAnalysis6.html',{'user':user})

def Eduexp1(request):
	if request.method=="POST":
		sy=int(request.POST.get("startyear"))
		ey=int(request.POST.get("endyear")) 
		Dataset=pd.read_csv("Education GDP.csv")

		# Filter the dataset for years between sy and ey
		Dataset_filtered = Dataset[(Dataset['Year'] >= sy) & (Dataset['Year'] <= ey)]

		# Create a grouped bar chart using Plotly
		fig = px.bar(
		    Dataset_filtered,
		    x='Entity',
		    y='Expenditure GDP',
		    color='Year',
		    barmode='group',
		    labels={'Expenditure GDP': 'Expenditure (% of GDP)', 'Entity': 'Country'},
		    color_discrete_sequence=px.colors.qualitative.Set2
		)

		# Update layout for the bar chart, including the year range
		fig.update_layout(
		    title=dict(text=f'Education Expenditure by Range Of Year ({sy}-{ey})', x=0.5, font=dict(size=18, color='black')),
		    xaxis=dict(title='Country', tickangle=45),
		    yaxis=dict(title='Expenditure (% of GDP)'),
		    legend_title=dict(text='Year'),
		    plot_bgcolor='white',
		    paper_bgcolor='white',
		    font=dict(size=12),
		    margin=dict(l=40, r=40, t=60, b=40),
		    )

		graph=fig.to_html()
		data=pd.read_csv("Education GDP.csv")
		year=data["Year"].drop_duplicates().to_list()
		return render(request,'Eduexp1.html',{"graph":graph,"year":year})
	else:
		data=pd.read_csv("Education GDP.csv")
		year=data["Year"].drop_duplicates().to_list()
		return render(request,'Eduexp1.html',{"year":year})

def Eduexp2(request):
	Dataset=pd.read_csv("Education GDP.csv")
	avg_expenditure = Dataset.groupby('Entity')['Expenditure GDP'].mean().reset_index()

	top_5 = avg_expenditure.nlargest(5, 'Expenditure GDP')
	bottom_5 = avg_expenditure.nsmallest(5, 'Expenditure GDP')

	top_bottom_countries = pd.concat([top_5, bottom_5])
	filtered_data = Dataset[Dataset['Entity'].isin(top_bottom_countries['Entity'])]

	bar_chart = go.Figure()

	bar_chart.add_trace(go.Bar(
	    x=top_5['Entity'],
	    y=top_5['Expenditure GDP'],
	    name='Top 5 Countries',
	    marker_color='rgba(0, 128, 0, 0.6)',
	    marker_line=dict(color='green', width=1.5)
	))

	bar_chart.add_trace(go.Bar(
	    x=bottom_5['Entity'],
	    y=bottom_5['Expenditure GDP'],
	    name='Bottom 5 Countries',
	    marker_color='rgba(255, 0, 0, 0.6)',
	    marker_line=dict(color='red', width=1.5)
	))

	bar_chart.update_layout(
	    title=dict(text='Top 5 and Bottom 5 Countries in Education Expenditure (% of GDP)', x=0.5, font=dict(size=20, color='black')),
	    xaxis=dict(title='Country', showgrid=False),
	    yaxis=dict(title='Average Expenditure (% of GDP)', showgrid=True, gridcolor='lightgrey'),
	    plot_bgcolor='white',
	    paper_bgcolor='white',
	    font=dict(size=12),
	    margin=dict(l=50, r=50, t=80, b=50),

	)

	#bar_chart.show()
	bar_graph=bar_chart.to_html()
	line_chart = px.line(
	    filtered_data,
	    x='Year',
	    y='Expenditure GDP',
	    color='Entity',
	    title='Education Expenditure Trends Over Time for Top and Bottom Countries',
	    labels={'Expenditure GDP': 'Expenditure (% of GDP)', 'Year': 'Year'},
	    line_group='Entity',
	    color_discrete_sequence=px.colors.qualitative.Set1,
	    markers=True
	)

	line_chart.update_layout(
	    title=dict(text='Trends in Education Expenditure Over Time for Top and Bottom Countries', x=0.5, font=dict(size=20, color='black')),
	    xaxis=dict(title='Year', showgrid=True, gridcolor='lightgrey'),
	    yaxis=dict(title='Expenditure (% of GDP)', showgrid=True, gridcolor='lightgrey'),
	    plot_bgcolor='white',
	    paper_bgcolor='white',
	    font=dict(size=12),
	    margin=dict(l=50, r=50, t=80, b=50),
	    legend=dict(title='Country')
	)

	#line_chart.show()
	linegraph=line_chart.to_html()
	return render(request,"Eduexp2.html",{"bar_graph":bar_graph,"linegraph":linegraph})


def Eduexp3(request):
    # Load the dataset
    Dataset = pd.read_csv("Education GDP.csv")
    
    # Function to categorize income levels based on GDP
    def categorize_income(gdp):
        if gdp < 2:
            return 'Low-income'
        elif 2 <= gdp <= 5:
            return 'Middle-income'
        else:
            return 'High-income'

    # Apply the categorize_income function to the Expenditure GDP column
    Dataset['Income Level'] = Dataset['Expenditure GDP'].apply(categorize_income)

    # Group by Entity and Income Level, and calculate the average expenditure
    avg_expenditure = Dataset.groupby(['Entity', 'Income Level'])['Expenditure GDP'].mean().reset_index()

    # Get unique income levels
    income_levels = avg_expenditure['Income Level'].unique()

    # Define colors for each income level
    colors = {'Low-income': '#636EFA', 'Middle-income': '#EF553B', 'High-income': '#00CC96'}

    # Create a plotly figure
    fig = go.Figure()

    # Add a trace for each income level
    for income_level in income_levels:
        filtered_data = avg_expenditure[avg_expenditure['Income Level'] == income_level]
        fig.add_trace(go.Bar(
            x=filtered_data['Entity'],
            y=filtered_data['Expenditure GDP'],
            name=income_level,
            visible=True if income_level == 'Low-income' else False,
            marker_color=colors[income_level],
            marker_line_width=1,
            marker_line_color='black'
        ))

    # Add dropdown buttons to toggle between income levels
    fig.update_layout(
        updatemenus=[
            dict(
                buttons=list([
                    dict(label='Low-income',
                         method='update',
                         args=[{'visible': [True if level == 'Low-income' else False for level in income_levels]},
                               {'title': 'Average Education Expenditure by Country - Low-income'}]),
                    dict(label='Middle-income',
                         method='update',
                         args=[{'visible': [True if level == 'Middle-income' else False for level in income_levels]},
                               {'title': 'Average Education Expenditure by Country - Middle-income'}]),
                    dict(label='High-income',
                         method='update',
                         args=[{'visible': [True if level == 'High-income' else False for level in income_levels]},
                               {'title': 'Average Education Expenditure by Country - High-income'}])
                ]),
                direction="down",
                showactive=True,
                x=1,
                y=1,
                xanchor='right',
                yanchor='bottom'
            )
        ]
    )

    # Set layout options for the figure
    fig.update_layout(
        title='Average Education Expenditure by Country and Income Level',
        title_font=dict(size=20, color='darkblue'),
        xaxis_title='Country',
        yaxis_title='Average Expenditure (% of GDP)',
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(size=14),
        hovermode="x unified",
        height=600,
        width=1000
    )

    # Convert the figure to HTML
    graph = fig.to_html()

    # Return the rendered HTML with the graph
    return render(request, 'Eduexp3.html', {"graph": graph})

def Eduexp4(request):
    if request.method == "POST":
        sy = int(request.POST.get("selectyear"))  # Get the selected year from the form
        
        # Load the dataset
        Dataset = pd.read_csv("Education GDP.csv")
        
        # Function to plot a donut chart for top 10 countries in a specific year
        def plot_donut_top_10_countries(dataframe, year):
            # Filter the dataframe for the selected year
            df_filtered = dataframe[dataframe['Year'] == year]

            # Ensure the dataframe is sorted by 'Expenditure GDP' in descending order
            sorted_df = df_filtered.sort_values(by='Expenditure GDP', ascending=False)

            # Get the top 10 countries based on expenditure GDP
            top_10_df = sorted_df.head(10)

            # Create the donut chart using Plotly
            fig = px.pie(
                top_10_df,
                values='Expenditure GDP',
                names='Entity',
                title=f'Top 10 Countries by Expenditure GDP in {year}',
                hover_data={'Expenditure GDP': ':.2f'},
                hole=0.4  # This creates the donut effect by adding a hole in the middle
               
            )

            # Customize layout
            fig.update_traces(textinfo='percent+label', pull=[0.05]*10, marker=dict(line=dict(color='deeppink', width=2)))

            # Add year inside the donut hole
            fig.update_layout(
		    showlegend=True, 
		    height=480,  # Adjust the height here
		    title_x=0.5,
		    annotations=[
        dict(text=f'{year}', x=0.5, y=0.5, font_size=20, showarrow=False),
        dict(text='Expenditure', x=0.5, y=0.4, font_size=16, showarrow=False),
    ]
)


            return fig  # Return the figure

        # Call the function to generate the figure
        fig = plot_donut_top_10_countries(Dataset, sy)

        # Convert the figure to HTML for rendering in the template
        graph = fig.to_html()

        # Fetch the unique years for the dropdown
        years = Dataset['Year'].drop_duplicates().to_list()

        # Render the template with the graph and years
        return render(request, 'Eduexp4.html', {"graph": graph, "year": years})
    
    else:
        # Load the dataset to get the list of years
        Dataset = pd.read_csv("Education GDP.csv")

        # Fetch the unique years for the dropdown
        years = Dataset['Year'].drop_duplicates().to_list()

        # Render the template with the year options (no graph)
        return render(request, 'Eduexp4.html', {"year": years})

def Eduexp5(request):
    # Load the dataset
    df = pd.read_csv("Education GDP.csv")

    # If the request method is POST, get the country name and generate the graph
    if request.method == "POST":
        country_name = request.POST.get("country_name")  # Get the country name from the POST request

        # Filter the DataFrame for the specific country
        country_data = df[df['Entity'] == country_name]

        # Extract the years and expenditure for plotting
        years = country_data['Year']
        expenditure = country_data['Expenditure GDP']

        # Create the plot using Plotly
        fig = go.Figure()

        # Scatter plot
        fig.add_trace(go.Scatter(
            x=years,
            y=expenditure,
            mode='markers',
            marker=dict(color='blue', size=10, line=dict(width=2, color='white')),
            name='Expenditure',
            text=[f"Year: {year}<br>Expenditure: {exp:.2f}%" for year, exp in zip(years, expenditure)],  # Hover info
            hoverinfo='text'  # Hover will display the text above
        ))

        # Line plot
        fig.add_trace(go.Scatter(
            x=years,
            y=expenditure,
            mode='lines',
            line=dict(color='red', width=2),
            name='Trend Line'
        ))

        # Customize layout
        fig.update_layout(
            title=f'Education Expenditure Over Time for {country_name}',
            xaxis_title='Year',
            yaxis_title='Expenditure (% of GDP)',
            template='plotly',
            hovermode='x unified',
            showlegend=True,
            legend=dict(x=0.05, y=1),
            height=500
        )

        # Return the graph as HTML
        graph = fig.to_html()

        # Prepare the list of countries for the dropdown
        countries = df['Entity'].drop_duplicates().tolist()

        # Render the template with the graph and country list
        return render(request, 'Eduexp5.html', {'graph': graph, 'countries': countries})

    else:
        # If not a POST request, render the template without the graph but with the country list
        countries = df['Entity'].drop_duplicates().tolist()
        return render(request, 'Eduexp5.html', {'countries': countries})



# Function to plot scatter plot with a line using Plotly
def plot_scatter_with_line(df, country_name):
    # Filter the DataFrame for the specific country
    country_data = df[df['Entity'] == country_name]

    # Check if there's data for the country
    if country_data.empty:
        return f"<p>No data available for country: {country_name}</p>"

    # Extract the years and expenditure for plotting
    years = country_data['Year']
    expenditure = country_data['Expenditure GDP']

    # Create the plot using Plotly
    fig = go.Figure()

    # Scatter plot
    fig.add_trace(go.Scatter(
        x=years,
        y=expenditure,
        mode='markers',
        marker=dict(color='blue', size=10, line=dict(width=2, color='white')),
        name='Expenditure',
        text=[f"Year: {year}<br>Expenditure: {exp:.2f}%" for year, exp in zip(years, expenditure)],  # Hover info
        hoverinfo='text'  # Hover will display the text above
    ))

    # Line plot
    fig.add_trace(go.Scatter(
        x=years,
        y=expenditure,
        mode='lines',
        line=dict(color='red', width=2),
        name='Trend Line'
    ))

    # Customize layout
    fig.update_layout(
        title=f'Education Expenditure Over Time for {country_name}',
        xaxis_title='Year',
        yaxis_title='Expenditure (% of GDP)',
        template='plotly',
        hovermode='x unified',
        showlegend=True,
        legend=dict(x=0.05, y=1),
        height=500
    )

    # Return the graph as HTML
    return fig.to_html()

def Eduexp6(request):
    # Load the data
    data = pd.read_csv('Education GDP.csv')

    # Function to plot year-to-year growth and loss using Plotly
    def plot_expenditure_growth_loss_scatter_line(dataframe, top_n=6):
        # Calculate total expenditure for each state
        total_expenditure = dataframe.groupby('Entity')['Expenditure GDP'].sum()

        # Get the top N states based on total expenditure
        top_states = total_expenditure.nlargest(top_n).index

        # Create a new plotly figure
        fig = go.Figure()

        # Plot for each top state
        for state_name in top_states:
            # Filter the dataframe for the given state name
            df_filtered = dataframe[dataframe['Entity'] == state_name]

            # Sort data by year
            df_filtered = df_filtered.sort_values(by='Year')

            # Extract years and expenditure GDP values
            years = df_filtered['Year']
            expenditures = df_filtered['Expenditure GDP']

            # Calculate the year-to-year change
            change = expenditures.diff().fillna(0)  # Fill missing values with 0 for the first year

            # Scatter plot
            fig.add_trace(go.Scatter(
                x=years,
                y=change,
                mode='markers+lines',
                marker=dict(size=8, line=dict(width=1, color='DarkSlateGrey')),
                line=dict(dash='solid', width=2),
                name=f'{state_name} - Change',
                text=[f"Year: {year}<br>Change: {chg:.2f}%" for year, chg in zip(years, change)],  # Hover info
                hoverinfo='text'  # Display text on hover
            ))

        # Customize layout
        fig.update_layout(
            title=f'Year-to-Year Growth and Loss of Expenditure GDP for Top {top_n} Countries',
            xaxis_title='Year',
            yaxis_title='Year-to-Year Change in Expenditure GDP (%)',
            template='plotly',
            hovermode='x unified',
            legend_title='Country',
            height=600,
            legend=dict(x=1, y=1, traceorder='normal')
        )

        # Return the plot as HTML
        return fig.to_html()

    # Plot for the top 6 states and pass it to the template
    graph = plot_expenditure_growth_loss_scatter_line(data, top_n=6)
    return render(request, 'Eduexp6.html', {"graph": graph})


def EduLit1(request):
    # Example usage with your updated dataset
    data = pd.read_csv("Literacy_Rate.csv")

    # Function to create a choropleth map of average literacy rates by country over all years
    def plot_avg_literacy_rate_choropleth(data):
        # Convert data to a pandas DataFrame
        df = pd.DataFrame(data, columns=['Entity', 'Code', 'Year', 'Literacy Rate'])

        # Group by 'Entity' and 'Code' to get the average literacy rate per country across all years
        avg_literacy_df = df.groupby(['Entity', 'Code'], as_index=False).agg({
            'Literacy Rate': 'mean',
            'Year': lambda x: ', '.join(map(str, sorted(x.unique())))  # Keep track of all unique years
        })

        # Create the choropleth map using Plotly Express
        fig = px.choropleth(
            avg_literacy_df,
            locations='Code',  # Use country codes
            color='Literacy Rate',
            hover_name='Entity',
            hover_data={'Literacy Rate': True, 'Year': True},  # Include years in the hover mode
            color_continuous_scale='Viridis',  # Use a different color scale
            title='Global Average Literacy Rates by Country',
            labels={'Literacy Rate': 'Average Literacy Rate (%)'}
        )

        # Update layout for better visualization
        fig.update_layout(
            geo=dict(
                showcoastlines=True,
                coastlinecolor="Black",
                projection_type="natural earth"  # Set projection type here
            ),
            coloraxis_colorbar=dict(title='Average Literacy Rate (%)'),
            title_x=0.5  # Center the title
        )

        # Convert the figure to HTML for rendering in the template
        return fig.to_html()

    # Generate the graph
    graph = plot_avg_literacy_rate_choropleth(data)

    # Render the template with the graph
    return render(request, 'EduLit1.html', {"graph": graph})


def EduLit2(request):
    # Load the dataset
    data = pd.read_csv("Literacy_Rate.csv")

    # Fetch the unique years for the dropdown
    years = data['Year'].drop_duplicates().to_list()

    if request.method == "POST":
        sy = int(request.POST.get("selectyear"))  # Get the selected year from the form

        # Function to create an interactive pie chart of literacy rates for a specific year
        def plot_literacy_rate_pie(data, year, top_n=10):
            # Convert data to a pandas DataFrame
            df = pd.DataFrame(data, columns=['Entity', 'Code', 'Year', 'Literacy Rate'])

            # Filter the data for the specified year
            df_year = df[df['Year'] == year]

            # Select the top_n countries by literacy rate
            df_top = df_year.nlargest(top_n, 'Literacy Rate')

            # Create the pie chart using Plotly Express
            fig = px.pie(df_top,
                         names='Entity',
                         values='Literacy Rate',
                         title=f'Top {top_n} Countries by Literacy Rate for {year}',
                         labels={'Literacy Rate': 'Literacy Rate (%)'},
                         color='Entity',  # Different colors for each country
                         hole=0.3,  # Create a donut chart
                         hover_data=['Literacy Rate']  # Show literacy rates on hover
                        )

            # Update layout for better visualization and interaction
            fig.update_layout(
                title_x=0.5,  # Center the title
                uniformtext_minsize=12,
                uniformtext_mode='hide',
                hoverlabel=dict(font_size=14, font_family="Rockwell"),
                legend_title_text='Country',
                annotations=[dict(
                    text=str(year),  # Display the year in the center of the pie chart
                    x=0.5, y=0.5, font_size=20, showarrow=False, font_color='black'
                )]
            )

            # Update hover template for better display of country and literacy rate
            fig.update_traces(
                hovertemplate="<b>%{label}</b><br>Literacy Rate: %{value}%",
                textinfo='label+percent',  # Show label and percent on the pie slices
                pull=[0.02]*len(df_top),  # Add some space between slices for better interaction
                marker=dict(line=dict(color='white', width=2))  # Add white borders for better visibility
            )

            # Return the plot as HTML
            return fig.to_html()

        # Generate the pie chart for the selected year
        graph = plot_literacy_rate_pie(data, sy)

        # Render the template with the graph and the years dropdown
        return render(request, 'EduLit2.html', {"graph": graph, "years": years})

    # In case the request method is not POST, render the page without a graph
    return render(request, 'EduLit2.html', {"years": years})

def EduLit3(request):
    # Load the dataset
    data = pd.read_csv("Literacy_Rate.csv")

    # Function to create an interactive grouped bar chart for literacy rates
    def plot_literacy_rate_bar(data, selected_countries):
        # Convert data to a pandas DataFrame
        df = pd.DataFrame(data, columns=['Entity', 'Code', 'Year', 'Literacy Rate'])

        # Filter the DataFrame for the selected countries
        filtered_df = df[df['Entity'].isin(selected_countries)]

        # Create the interactive grouped bar chart using Plotly Express
        fig = px.bar(
            filtered_df,
            x='Entity',
            y='Literacy Rate',
            color='Year',  # Group bars by year
            barmode='group',  # Display bars grouped by year
            hover_name='Entity',  # Display country name on hover
            title='Literacy Rate Comparison by Multiple Country and Year',
            labels={'Literacy Rate': 'Literacy Rate (%)', 'Entity': 'Country'},
            color_discrete_sequence=px.colors.qualitative.Bold  # Different color set for more variation
        )

        # Add interactivity by updating hover info, adding bar gaps, and customizing colors
        fig.update_traces(
            hovertemplate='<b>%{x}</b><br>Year: %{customdata[0]}<br>Literacy Rate: %{y}%',
            customdata=filtered_df[['Year']].values,
            marker_line_width=1.5,  # Add a border to bars for better visual effect
            marker_line_color='black'
        )

        # Add interactivity to allow filtering by country using the legend
        fig.update_layout(
            legend=dict(
                title="Year",
                font=dict(size=12),
                orientation="h",  # Display legend horizontally
                yanchor="bottom",
                y=-0.3,
                xanchor="center",
                x=0.5
            ),
            hoverlabel=dict(font_size=12, font_family="Arial"),  # Customize hover label appearance
            title_x=0.5  # Center the title
        )

        # Return the plot as HTML
        return fig.to_html()

    # Define the selected countries (20 countries)
    selected_countries = [
        'Afghanistan', 'Albania', 'Zimbabwe', 'India', 'France', 'Germany', 'China', 'Brazil',
        'Canada', 'Mexico', 'Japan', 'Australia', 'South Korea', 'United States', 'Russia',
        'Italy', 'Spain', 'Argentina', 'Chile', 'Peru'
    ]

    # Generate the grouped bar chart for the selected countries
    graph = plot_literacy_rate_bar(data, selected_countries)

    # Render the template with the generated graph
    return render(request, 'EduLit3.html', {"graph": graph})

def EduLit4(request):
    # Load the dataset
    data = pd.read_csv("Literacy_Rate.csv")

    if request.method == "POST":
        # Get start year and end year from the POST request
        start_year = int(request.POST.get("startyear"))
        end_year = int(request.POST.get("endyear"))

        # Function to create a bar chart for top and bottom 5 countries by average growth between specific start and end years
        def plot_top_bottom_countries_growth_bar_chart(data, start_year, end_year):
            # Convert data to a pandas DataFrame
            df = pd.DataFrame(data, columns=['Entity', 'Code', 'Year', 'Literacy Rate'])

            # Ensure 'Year' column is numeric
            if not pd.api.types.is_numeric_dtype(df['Year']):
                try:
                    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
                except Exception as e:
                    print("Error converting 'Year' to numeric:", e)
                    raise

            # Filter the DataFrame for the specified start and end years
            df_filtered = df[(df['Year'] >= start_year) & (df['Year'] <= end_year)]

            # Group by 'Entity' and calculate the average literacy rate within this period
            avg_growth_df = df_filtered.groupby('Entity').agg({'Literacy Rate': 'mean'}).reset_index()
            avg_growth_df.columns = ['Entity', 'Average Literacy Rate']

            # Get the top 5 countries with the highest average literacy rate
            top_5_growth = avg_growth_df.nlargest(5, 'Average Literacy Rate')
            # Get the bottom 5 countries with the lowest average literacy rate
            bottom_5_growth = avg_growth_df.nsmallest(5, 'Average Literacy Rate')

            # Combine top and bottom 5 into a single DataFrame for easier plotting
            top_bottom_growth = pd.concat([top_5_growth, bottom_5_growth])
            top_bottom_growth['Country Group'] = ['Top Growth'] * len(top_5_growth) + ['Bottom Growth'] * len(bottom_5_growth)

            # Reset index for easy plotting
            top_bottom_growth.reset_index(inplace=True, drop=True)

            # Create the bar chart for average growth rates
            fig = px.bar(
                top_bottom_growth,
                x='Entity',
                y='Average Literacy Rate',
                color='Country Group',
                title=f'Top 5 and Bottom 5 Countries by Average Literacy Rate ({start_year}-{end_year})',
                labels={'Average Literacy Rate': 'Average Literacy Rate (%)', 'Entity': 'Country'},
                text='Average Literacy Rate',  # Display average rate on the bars
                barmode='group',  # Separate the top and bottom growth
                color_discrete_sequence=px.colors.qualitative.Bold  # Different color set for more variation
            )

            # Customize hover info and layout
            fig.update_traces(
                hovertemplate=(
                    '<b>Country:</b> %{x}<br>'
                    '<b>Average Literacy Rate:</b> %{y:.2f}%<br>'
                    f'<b>Years:</b> {start_year}-{end_year}'
                ),
                texttemplate='%{text:.2f}%',  # Show text labels on bars
                textposition='outside'  # Place the text outside the bars
            )

            # Add interactivity to allow filtering by country using the legend
            fig.update_layout(
                legend=dict(
                    title="Country Group",
                    font=dict(size=12),
                    orientation="h",  # Display legend horizontally
                    yanchor="bottom",
                    y=-0.3,
                    xanchor="center",
                    x=0.5
                ),
                hoverlabel=dict(font_size=12, font_family="Arial"),  # Customize hover label appearance
                title_x=0.5  # Center the title
            )
            # Return the plot as HTML
            return fig.to_html()  # Return the graph here

        # Call the function to create the graph
        graph = plot_top_bottom_countries_growth_bar_chart(data, start_year, end_year)

        # Get the list of unique years from the dataset
        year = data["Year"].drop_duplicates().to_list()

        # Render the HTML template with the graph and year data
        return render(request, 'EduLit4.html', {"graph": graph, "year": year})

    else:
        # If not a POST request, just return the list of years
        year = data["Year"].drop_duplicates().to_list()
        return render(request, 'EduLit4.html', {"year": year})

# def EduLit5(request):
#     # Load the dataset
#     data = pd.read_csv("Literacy_Rate.csv")

#     # Extract unique countries and years for the dropdown menu
#     countries = sorted(data['Entity'].dropna().unique())
#     years = sorted(data['Year'].dropna().unique().astype(int))

#     if request.method == "POST":
#         # Get selected values from the form
#         start_year = int(request.POST.get("startyear"))
#         end_year = int(request.POST.get("endyear"))
#         country = request.POST.get("country_name")

#         # Function to create an interactive area chart for one country with a specified year range
#         def plot_country_growth_area_chart(data, country, start_year, end_year):
#             # Convert data to a pandas DataFrame
#             df = pd.DataFrame(data, columns=['Entity', 'Code', 'Year', 'Literacy Rate'])

#             # Ensure 'Year' column is numeric
#             if not pd.api.types.is_numeric_dtype(df['Year']):
#                 df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

#             # Filter the DataFrame for the selected country and the specified year range
#             filtered_df = df[(df['Entity'] == country) & (df['Year'] >= start_year) & (df['Year'] <= end_year)]

#             if filtered_df.empty:
#                 return "<p>No data available for the selected country and year range.</p>"

#             # Create the interactive area chart using Plotly Express
#             fig = px.area(
#                 filtered_df,
#                 x='Year',
#                 y='Literacy Rate',
#                 title=f'Literacy Rate Growth of {country} ({start_year}-{end_year})',
#                 labels={'Literacy Rate': 'Literacy Rate (%)', 'Year': 'Year'},
#                 color_discrete_sequence=px.colors.qualitative.Bold
#             )

#             # Customize hover info and layout
#             fig.update_traces(
#                 hovertemplate='<b>Country:</b> ' + country + '<br><b>Year:</b> %{x}<br><b>Literacy Rate:</b> %{y}%',
#                 line=dict(width=2)
#             )

#             # Add layout customizations
#             fig.update_layout(
#                 hoverlabel=dict(font_size=12, font_family="Arial"),
#                 title_x=0.5
#             )

#             # Return the plot as HTML
#             return fig.to_html()

#         # Generate the area chart graph for the selected country and year range
#         graph = plot_country_growth_area_chart(data, country, start_year, end_year)

#         # Render the template with the graph, countries, and years
#         return render(request, 'EduLit5.html', {
#             'graph': graph,
#             'country': countries,
#             'years': years,
#             'selected_country': country,
#             'selected_start_year': start_year,
#             'selected_end_year': end_year
#         })

#     # If not a POST request, render the form
#     return render(request, 'EduLit5.html', {
#         'country': countries,
#         'years': years
#     })


# # Function to create an interactive area chart for one country with specified year range
# def EduLit5(country, start_year, end_year):
# 	 data = pd.read_csv("Literacy_Rate.csv")

# 	  # Extract unique countries and years for the dropdown menu
#     countries = sorted(data['Entity'].dropna().unique())
#     years = sorted(data['Year'].dropna().unique().astype(int))

#     if request.method == "POST":
#         # Get selected values from the form
#         start_year = int(request.POST.get("startyear"))
#         end_year = int(request.POST.get("endyear"))
#         country = request.POST.get("country_name")

#     # Convert data to a pandas DataFrame
#     df = pd.DataFrame(data, columns=['Entity', 'Code', 'Year', 'Literacy Rate'])

#     # Ensure 'Year' column is numeric
#     if not pd.api.types.is_numeric_dtype(df['Year']):
#         try:
#             df['Year'] = pd.to_numeric(df['Year'], errors='coerce')
#         except Exception as e:
#             print("Error converting 'Year' to numeric:", e)
#             raise

#     # Filter the DataFrame for the selected country and the specified year range
#     filtered_df = df[(df['Entity'] == country) & (df['Year'] >= start_year) & (df['Year'] <= end_year)]

#     # Create the interactive area chart using Plotly Express
#     fig = px.area(
#         filtered_df,
#         x='Year',
#         y='Literacy Rate',
#         title=f'Literacy Rate Growth of {country} By Year ({start_year}-{end_year})',
#         labels={'Literacy Rate': 'Literacy Rate (%)', 'Year': 'Year'},
#         color_discrete_sequence=px.colors.qualitative.Bold  # Single color for the country
#     )

#     # Customize hover info and layout
#     fig.update_traces(
#         hovertemplate='<b>Country:</b> ' + country + '<br><b>Year:</b> %{x}<br><b>Literacy Rate:</b> %{y}%',
#         line=dict(width=2)  # Customize line width
#     )

#     # Add layout customizations
#     fig.update_layout(
#         hoverlabel=dict(font_size=12, font_family="Arial"),  # Customize hover label appearance
#         title_x=0.5  # Center the title
#     )

#      # Return the plot as HTML
#             return fig.to_html()

#         # Generate the area chart graph for the selected country and year range
#         graph = plot_country_growth_area_chart(data, country, start_year, end_year)

#         # Render the template with the graph, countries, and years
#         return render(request, 'EduLit5.html', {
#             'graph': graph,
#             'country': countries,
#             'years': years,
#             'selected_country': country,
#             'selected_start_year': start_year,
#             'selected_end_year': end_year
#         })

#     # If not a POST request, render the form
#     return render(request, 'EduLit5.html', {
#         'country': countries,
#         'years': years
#     })


     # Function to create an interactive area chart for a country with a specified year range
def EduLit5(request):
    # Load the dataset
    data = pd.read_csv("Literacy_Rate.csv")

    # Extract unique countries and years for the dropdown menu
    countries = sorted(data['Entity'].dropna().unique())
    years = sorted(data['Year'].dropna().unique().astype(int))

    if request.method == "POST":
        # Get selected values from the form
        start_year = int(request.POST.get("startyear"))
        end_year = int(request.POST.get("endyear"))
        country = request.POST.get("country_name")

        # Convert data to a pandas DataFrame
        df = pd.DataFrame(data, columns=['Entity', 'Code', 'Year', 'Literacy Rate'])

        # Ensure 'Year' column is numeric
        if not pd.api.types.is_numeric_dtype(df['Year']):
            df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

        # Filter the DataFrame for the selected country and year range
        filtered_df = df[(df['Entity'] == country) & (df['Year'] >= start_year) & (df['Year'] <= end_year)]

        if filtered_df.empty:
            # Return an error message if no data is available
            return render(request, 'EduLit5.html', {
                'error_message': f'No data available for {country} from {start_year} to {end_year}.',
                'country': countries,
                'years': years,
                'selected_country': country,
                'selected_start_year': start_year,
                'selected_end_year': end_year
            })

        # Create the interactive area chart using Plotly Express
        fig = px.area(
            filtered_df,
            x='Year',
            y='Literacy Rate',
            title=f'Literacy Rate Growth of {country} ({start_year}-{end_year})',
            labels={'Literacy Rate': 'Literacy Rate (%)', 'Year': 'Year'},
            color_discrete_sequence=px.colors.qualitative.Bold
        )

        # Customize hover info and layout
        fig.update_traces(
            hovertemplate='<b>Country:</b> ' + country + '<br><b>Year:</b> %{x}<br><b>Literacy Rate:</b> %{y}%',
            line=dict(width=2)
        )

        # Add layout customizations
        fig.update_layout(
            hoverlabel=dict(font_size=12, font_family="Arial"),
            title_x=0.5
        )

        # Return the plot as HTML
        graph = fig.to_html()

        # Render the template with the graph and form values
        return render(request, 'EduLit5.html', {
            'graph': graph,
            'country': countries,
            'years': years,
            'selected_country': country,
            'selected_start_year': start_year,
            'selected_end_year': end_year
        })

    # If not a POST request, render the form
    return render(request, 'EduLit5.html', {
        'country': countries,
        'years': years
    })

def EduLit6(request):
    # Load the dataset
    data = pd.read_csv("Literacy_Rate.csv")

    # Prepare the list of countries for the dropdown
    countries = data['Entity'].drop_duplicates().tolist()

    # If the request method is POST, get the country name and generate the graph
    if request.method == "POST":
        country_name = request.POST.get("country_name")  # Get the country name from the POST request

        # Function to analyze literacy trends over decades with a stacked area chart for specific countries
        def analyze_literacy_trends_stacked_area(df, countries):
            # Create a new column for decades
            df['Decade'] = (df['Year'] // 10) * 10

            # Filter data for the selected countries
            df_filtered = df[df['Entity'].isin(countries)].copy()

            # Group by Decade and Entity (Country) and calculate average literacy rate per decade
            literacy_by_decade = df_filtered.groupby(['Decade', 'Entity'])['Literacy Rate'].mean().reset_index()

            # Create a stacked area chart using Plotly
            fig = px.area(literacy_by_decade, x='Decade', y='Literacy Rate', color='Entity',
                          title=f"Literacy Rate Trends in {', '.join(countries)} Over Decades",
                          labels={'Decade': 'Decade', 'Literacy Rate': 'Average Literacy Rate (%)'},
                          markers=True,
                          template="plotly_white")

            # Customize the layout
            fig.update_layout(
                xaxis=dict(showgrid=True, gridcolor='black', gridwidth=0.5),
                yaxis=dict(range=[0, 100], showgrid=True, gridcolor='black', gridwidth=0.5),
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(size=14)
            )

            # Return the graph as HTML
            return fig.to_html()

        # Define the list of countries to include in the analysis
        selected_countries = [country_name]

        # Generate the graph using the selected country
        graph = analyze_literacy_trends_stacked_area(data, selected_countries)

        # Render the template with the graph and country list
        return render(request, 'EduLit6.html', {'graph': graph, 'countries': countries})

    else:
        # If not a POST request, render the template without the graph but with the country list
        return render(request, 'EduLit6.html', {'countries': countries})

def EduEnrollP1(request):
    # Load the dataset
    file_path = "School Enrollment (Primary).csv"
    df = pd.read_csv(file_path)

    # Melt the dataset to create a year column
    melted_df = df.melt(id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'],
                        var_name='Year', value_name='Enrollment Rate')

    # Convert 'Enrollment Rate' to numeric
    melted_df['Enrollment Rate'] = pd.to_numeric(melted_df['Enrollment Rate'], errors='coerce')

    # Find the minimum and maximum enrollment rate for each country along with the corresponding years
    min_enrollment = melted_df.loc[melted_df.groupby('Country Name')['Enrollment Rate'].idxmin()]
    max_enrollment = melted_df.loc[melted_df.groupby('Country Name')['Enrollment Rate'].idxmax()]

    # Rename columns for clarity
    min_enrollment = min_enrollment.rename(columns={'Year': 'Year_min', 'Enrollment Rate': 'Enrollment Rate_min'})
    max_enrollment = max_enrollment.rename(columns={'Year': 'Year_max', 'Enrollment Rate': 'Enrollment Rate_max'})

    # Combine the min and max data
    min_max_enrollment = pd.merge(min_enrollment[['Country Name', 'Year_min', 'Enrollment Rate_min']],
                                  max_enrollment[['Country Name', 'Year_max', 'Enrollment Rate_max']],
                                  on='Country Name')

    # Reshape the data for plotting
    plot_data = pd.melt(min_max_enrollment,
                        id_vars=['Country Name', 'Year_min', 'Year_max'],
                        value_vars=['Enrollment Rate_min', 'Enrollment Rate_max'],
                        var_name='Rate Type',
                        value_name='Enrollment Rate')

    # Add corresponding years
    plot_data['Year'] = plot_data.apply(lambda row: row['Year_min'] if row['Rate Type'] == 'Enrollment Rate_min' else row['Year_max'], axis=1)

    # Create a bar chart to visualize the minimum and maximum enrollment rates with years
    fig = px.bar(plot_data,
                 x='Country Name',
                 y='Enrollment Rate',
                 color='Rate Type',
                 title='Minimum and Maximum Primary School Enrollment Rates by Country',
                 text='Year',
                 barmode='group')

    # Customize the layout
    fig.update_layout(xaxis_title='Country',
                      yaxis_title='Enrollment Rate (%)',
                      legend_title_text='Rate Type')

    # Convert the figure to HTML format for rendering
    graph = fig.to_html()

    # Render the template with the graph
    return render(request, 'EduEnroll1 (Primary).html', {'graph': graph})


def EduEnrollP2(request):
    # Load the dataset
    df = pd.read_csv("School Enrollment (Primary).csv")

    # Define the years of interest
    years = [str(year) for year in range(2000, 2018)]

    # Function to create the plot
    def plot_school_enrollment(df, country_name, years):
        # Filter the DataFrame for the specific country
        country_data = df[df['Country Name'] == country_name]

        # Select relevant columns and drop rows with NaN values in 'School enrollment, primary (% net)'
        country_data = country_data[['Country Name'] + years].dropna(subset=years)

        # Melt the DataFrame to long format for Plotly
        country_data_long = country_data.melt(id_vars='Country Name', var_name='Year', value_name='Enrollment Rate')

        # Create the line plot
        fig = px.line(
            country_data_long,
            x='Year',
            y='Enrollment Rate',
            title=f'Primary School Enrollment Rate in {country_name}',
            labels={'Enrollment Rate': 'Enrollment Rate (%)'},
            markers=True
        )

        # Update layout to show years on the x-axis
        fig.update_layout(
            xaxis_title='Year',
            yaxis_title='Enrollment Rate (%)',
            xaxis=dict(tickvals=[str(year) for year in years], ticktext=[str(year) for year in years])
        )

        return fig

    # If the request method is POST, get the country name and generate the graph
    if request.method == "POST":
        country_name = request.POST.get("country_name")  # Get the country name from the POST request

        # Generate the graph for the selected country
        fig = plot_school_enrollment(df, country_name, years)
        graph = fig.to_html()

        # Prepare the list of countries for the dropdown
        countries = df['Country Name'].drop_duplicates().tolist()

        # Render the template with the graph and country list
        return render(request, 'EduEnroll2 (Primary).html', {'graph': graph, 'countries': countries})

    else:
        # If not a POST request, render the template without the graph but with the country list
        countries = df['Country Name'].drop_duplicates().tolist()
        return render(request, 'EduEnroll2 (Primary).html', {'countries': countries})

def EduEnrollP3(request):
    # Load your dataset
    df = pd.read_csv("School Enrollment (Primary).csv")

    # List of countries and years for the dropdowns
    countries = df['Country Name'].unique().tolist()
    years = list(range(2000, 2017))  # Adjust based on available data

    # If it's a POST request, process the form data
    if request.method == "POST":
        # Extract form data
        country1 = request.POST.get("country1_name")
        country2 = request.POST.get("country2_name")
        start_year = int(request.POST.get("startyear"))
        end_year = int(request.POST.get("endyear"))

        # Function to generate the enrollment comparison plot
        def plot_comparison_enrollment(df, country1, country2, start_year, end_year):
            # Define the list of years based on the start and end years
            years = [str(year) for year in range(start_year, end_year + 1)]

            # Filter the DataFrame for the specific countries
            country1_data = df[df['Country Name'] == country1]
            country2_data = df[df['Country Name'] == country2]

            # Melt the data to a long format for both countries
            country1_long = country1_data[['Country Name'] + years].melt(id_vars='Country Name', var_name='Year', value_name='Enrollment Rate').assign(Country=country1)
            country2_long = country2_data[['Country Name'] + years].melt(id_vars='Country Name', var_name='Year', value_name='Enrollment Rate').assign(Country=country2)

            # Combine the data for both countries
            combined_data = pd.concat([country1_long, country2_long])

            # Create the line plot using Plotly Express
            fig = px.line(
                combined_data,
                x='Year',
                y='Enrollment Rate',
                color='Country',
                title=f'Primary School Enrollment Rate Comparison: {country1} vs {country2} ({start_year}-{end_year})',
                labels={'Enrollment Rate': 'Enrollment Rate (%)'},
                markers=True
            )

            # Update layout settings for better visualization
            fig.update_layout(
                xaxis_title='Year',
                yaxis_title='Enrollment Rate (%)',
                xaxis=dict(tickvals=years, ticktext=years),
                yaxis=dict(tickformat=".2f")
            )

            return fig

        # Generate the plot
        fig = plot_comparison_enrollment(df, country1, country2, start_year, end_year)
        graph = fig.to_html()

        # Render the template with the generated graph
        return render(request, 'EduEnroll3 (Primary).html', {
            'countries': countries,
            'year': years,
            'graph': graph
        })

    # For a GET request, render the form without a graph
    return render(request, 'EduEnroll3 (Primary).html', {
        'countries': countries,
        'year': years
    })

def EduEnrollP4(request):
    if request.method == "POST":
        # Get the selected year from the form
        sy = int(request.POST.get("selectyear"))

        # Load the dataset
        Dataset = pd.read_csv("School Enrollment (Primary).csv")

        # Function to generate the donut chart for a specific year
        def plot_donut_chart_for_year(df, year):
            year = str(year)

            # Filter the data for the specified year
            data_for_year = df[['Country Name', year]].rename(columns={year: 'Enrollment Rate'})

            # Drop any rows with missing data for the year
            data_for_year = data_for_year.dropna()

            # Get the top 12 countries by enrollment rate for the specified year
            top_countries = data_for_year.nlargest(12, 'Enrollment Rate')

            # Create the donut chart
            fig = go.Figure(data=[go.Pie(
                labels=top_countries['Country Name'],
                values=top_countries['Enrollment Rate'],
                hole=0.4,  # This creates the donut effect
                textinfo='label+percent',  # Show both the label and percentage
                marker=dict(line=dict(color='teal', width=2))  # Add border to the slices
            )])

            # Add a text annotation for the year in the center
            fig.add_annotation(
                text=str(year),
                showarrow=False,
                font=dict(size=24, color='black'),
                align='center',
                x=0.5,
                y=0.5
            )

            fig.update_layout(
                title=f'Top 12 Countries by Primary School Enrollment Rate ({year})',
                showlegend=True
            )

            return fig

        # Generate the donut chart for the selected year
        fig = plot_donut_chart_for_year(Dataset, sy)

        # Convert the figure to HTML for rendering in the template
        graph = fig.to_html()

        # Fetch the unique years for the dropdown
        years = [col for col in Dataset.columns if col.isdigit()]  # Extract years from column names

        # Render the template with the graph and years
        return render(request, 'EduEnroll4 (Primary).html', {"graph": graph, "year": years})

    else:
        # Load the dataset to get the list of years
        Dataset = pd.read_csv("School Enrollment (Primary).csv")

        # Fetch the unique years for the dropdown (filter column names that are years)
        years = [col for col in Dataset.columns if col.isdigit()]

        # Render the template with the year options (no graph)
        return render(request, 'EduEnroll4 (Primary).html', {"year": years})

def EduEnrollP5(request):
    if request.method == "POST":
        # Get start year and end year from the form
        sy = int(request.POST.get("startyear"))
        ey = int(request.POST.get("endyear"))

        # Load the dataset
        Dataset = pd.read_csv("School Enrollment (Primary).csv")

        # Define a function to plot the bar chart
        def plot_bar_chart(df, countries, start_year, end_year):
            # Ensure the years are in string format
            years = [str(year) for year in range(start_year, end_year + 1)]

            # Filter the data for the specified countries and years
            filtered_data = df[df['Country Name'].isin(countries)]
            data_for_years = filtered_data[['Country Name'] + years]

            # Melt the DataFrame to long format
            melted_data = data_for_years.melt(id_vars='Country Name', var_name='Year', value_name='Enrollment Rate')

            # Drop any rows with missing data
            melted_data = melted_data.dropna()

            # Create the bar chart with color differentiation
            fig = px.bar(
                melted_data,
                x='Country Name',
                y='Enrollment Rate',
                color='Year',  # Different colors for each year
                title=f'Primary School Enrollment Rates from {start_year} to {end_year}',
                labels={'Enrollment Rate': 'Enrollment Rate (%)', 'Year': 'Year'},
                facet_col='Year',  # Create separate subplots for each year
                facet_col_wrap=3,  # Wrap to 3 columns for better layout
                text="Country Name"
            )

            # Customize the layout for better visualization
            fig.update_layout(
                xaxis_title='Country',
                yaxis_title='Enrollment Rate (%)',
                xaxis=dict(tickangle=-45),
                height=800,  # Adjust the height to accommodate multiple subplots
                margin=dict(l=50, r=50, t=50, b=150)  # Adjust margins for better spacing
            )

            return fig

        # Define the countries you want to compare (you can update this as per your needs)
        selected_countries = ['Australia', 'Germany', 'Argentina', 'Austria', 'Switzerland', 'United Kingdom']

        # Generate the plot
        fig = plot_bar_chart(Dataset, selected_countries, sy, ey)

        # Convert the figure to HTML for rendering in the template
        graph = fig.to_html()

        # Fetch the unique years for the dropdown
        years = [col for col in Dataset.columns if col.isdigit()]  # Extract years from column names

        # Render the template with the graph and years
        return render(request, 'EduEnroll5 (Primary).html', {"graph": graph, "year": years})

    else:
        # Load the dataset to get the list of years
        Dataset = pd.read_csv("School Enrollment (Primary).csv")

        # Fetch the unique years for the dropdown (filter column names that are years)
        years = [col for col in Dataset.columns if col.isdigit()]

        # Render the template with the year options (no graph)
        return render(request, 'EduEnroll5 (Primary).html', {"year": years})


def EduEnrollP6(request):
    # Load the dataset from the CSV file
    Dataset1 = "School Enrollment (Primary).csv"
    df = pd.read_csv(Dataset1)

    # Define the countries of interest
    selected_countries = ['India', 'Spain', 'Norway', 'Switzerland', 'Australia', 'Germany', 'Austria']

    # Filter the DataFrame for the selected countries
    df_selected = df[df['Country Name'].isin(selected_countries)]

    # Select the years to visualize
    years = [str(year) for year in range(2000, 2018)]

    # Melt the DataFrame to have years as a column for plotting
    df_melted = df_selected.melt(id_vars=['Country Name'], value_vars=years,
                                 var_name='Year', value_name='Enrollment Rate')

    # Get the highest enrollment rate for each country
    df_max = df_melted.loc[df_melted.groupby('Country Name')['Enrollment Rate'].idxmax()]

    # Find the row with the overall highest enrollment rate
    df_highest = df_max.loc[df_max['Enrollment Rate'].idxmax()]

    # Plotting the bar chart for the highest rates with colors
    fig = px.bar(df_max, x='Country Name', y='Enrollment Rate',
                 color='Country Name',  # Color by Country Name
                 title='Highest Primary School Enrollment Rates',
                 labels={'Enrollment Rate': 'Enrollment Rate (%)'},
                 height=600,
                 hover_data={'Country Name': True, 'Enrollment Rate': True, 'Year': True})  # Include details in hover

    # Add annotation to highlight only the overall highest rate
    fig.add_annotation(x=df_highest['Country Name'], y=df_highest['Enrollment Rate'],
                       text=f"Highest: {df_highest['Enrollment Rate']:.2f}%",
                       showarrow=True, arrowhead=2,
                       arrowcolor='red', arrowsize=1.5, ax=0, ay=-40)

    # Convert the plot to HTML
    graph = fig.to_html()

    # Render the template with the graph
    return render(request, 'EduEnroll6 (Primary).html', {'graph': graph})

def EduPop1(request):
    if request.method == "POST":
        sy = int(request.POST.get("selectyear"))  # Get the selected year
        
        # Load your dataset
        data = pd.read_csv("Global Education (World Population).csv")
        df = pd.DataFrame(data)

        # Filter for selected countries for the selected year
        selected_countries = ["Afghanistan", "Albania", "Zimbabwe", "Algeria",
                              "Zambia", "India", "Brazil", "Mexico"]
        df_filtered = df[(df['Entity'].isin(selected_countries)) & (df['Year'] == sy)]

        # Melt the dataframe for plotting
        df_melted = df_filtered.melt(id_vars=["Entity", "Year"],
                                     value_vars=["Share of population (No Education)",
                                                 "Share of population (Basic Education)"],
                                     var_name="Education Level",
                                     value_name="Share")

        # Create a line chart with hover data including the Year
        fig = px.line(df_melted,
                      x="Entity",
                      y="Share",
                      color="Education Level",
                      title=f"Share of Population with No Education vs. Basic Education ({sy})",
                      labels={"Share": "Share of Population (%)", "Entity": "Country"},
                      markers=True,
                      hover_data={"Year": True})

        # Update layout for better readability
        fig.update_layout(yaxis_title="Share of Population (%)",
                          xaxis_title="Country",
                          legend_title="Education Level")

        # Show the plot
        graph = fig.to_html()

        # Fetch the unique years for the dropdown
        years = df['Year'].drop_duplicates().to_list()

        # Render the template with the graph and years
        return render(request, 'EduPop1.html', {"graph": graph, "year": years})

    else:
        # Load the dataset to get the list of years
        Dataset = pd.read_csv("Global Education (World Population).csv")

        # Fetch the unique years for the dropdown
        years = Dataset['Year'].drop_duplicates().to_list()

        # Render the template with the year options (no graph)
        return render(request, 'EduPop1.html', {"year": years})


def EduPop2(request):
    # Load the dataset only once
    data = pd.read_csv("Global Education (World Population).csv")
    df = pd.DataFrame(data)

    # Get the list of unique countries from the dataset for the dropdown
    countries = df['Entity'].unique().tolist()

    # If it's a POST request, process the form data
    if request.method == "POST":
        # Extract form data
        country1 = request.POST.get("country1_name")
        country2 = request.POST.get("country2_name")

        # Ensure both countries are selected
        if not country1 or not country2:
            return render(request, 'EduPop2.html', {
                'countries': countries,
                'error': "Please select both countries."
            })

        # Filter for the selected countries over all available years
        selected_countries = [country1, country2]
        df_filtered = df[df['Entity'].isin(selected_countries)]

        # Melt the DataFrame for visualization
        df_melted = df_filtered.melt(id_vars=["Entity", "Year"],
                                     value_vars=["Share of population (No Education)",
                                                 "Share of population (Basic Education)"],
                                     var_name="Education Level",
                                     value_name="Share")

        # Create a grouped bar chart
        fig = px.bar(df_melted,
                     x="Year",
                     y="Share",
                     color="Education Level",
                     barmode="group",  # Grouped bar mode
                     facet_col="Entity",  # Separate plots for each country
                     title=f"Share of Population with No Education vs. Basic Education for {country1} and {country2}",
                     labels={"Share": "Share of Population (%)", "Year": "Year", "Education Level": "Education Level"})

        # Update layout for better readability
        fig.update_layout(yaxis_title="Share of Population (%)",
                          xaxis_title="Year",
                          legend_title="Education Level")

        # Convert the figure to HTML for rendering in the template
        graph = fig.to_html()

        # Render the template with the generated graph
        return render(request, 'EduPop2.html', {
            'countries': countries,
            'graph': graph
        })

    # For a GET request, render the form without a graph
    return render(request, 'EduPop2.html', {
        'countries': countries,
    })

def EduPop3(request):
    # Load the dataset once
    data = pd.read_csv("Global Education (World Population).csv")
    df = pd.DataFrame(data)

    # Get the list of unique countries for the dropdown
    countries = df['Entity'].drop_duplicates().tolist()

    # If the request method is POST, get the country name and generate the graph
    if request.method == "POST":
        # Get the country name from the POST request
        country_name = request.POST.get("country_name")

        # Ensure a country is selected
        if not country_name:
            return render(request, 'EduPop3.html', {
                'countries': countries,
                'error': "Please select a country."
            })

        # Filter the data for the selected country
        filtered_df = df[df['Entity'] == country_name]

        # Prepare data for the donut chart
        # Summing shares for each year and education level
        donut_data = filtered_df.groupby('Year').agg({
            'Share of population (No Education)': 'sum',
            'Share of population (Basic Education)': 'sum'
        }).reset_index()

        # Add the country name to the dataset for hover data
        donut_data['Country'] = country_name

        # Melt the DataFrame for plotting
        donut_melted = donut_data.melt(id_vars=['Year', 'Country'],
                                       value_vars=['Share of population (No Education)',
                                                   'Share of population (Basic Education)'],
                                       var_name='Education Level',
                                       value_name='Share')

        # Create a faceted donut chart for all years
        fig = px.pie(donut_melted,
                     values='Share',
                     names='Education Level',
                     title=f'Education Levels in {country_name} (All Years)',
                     hole=0.4,
                     facet_col='Year',  # Create subplots based on Year
                     facet_col_wrap=3,  # Adjust the number of donut charts per row
                     hover_data={'Country': True})  # Show country name in hover data

        # Convert the figure to HTML for rendering in the template
        graph = fig.to_html()

        # Render the template with the generated graph and the country list
        return render(request, 'EduPop3.html', {
            'graph': graph,
            'countries': countries
        })

    # If not a POST request, render the template without the graph but with the country list
    return render(request, 'EduPop3.html', {'countries': countries})

def EduPop4(request):
    # Load your dataset inside the function
    data = pd.read_csv("Global Education (World Population).csv")
    df = pd.DataFrame(data)

    # Select 10 specific countries
    selected_countries = ["India", "Brazil", "Algeria", "Albania",
                          "Afghanistan", "Zimbabwe", "Zambia",
                          "Mexico", "Spain", "Germany", "Australia"]

    # Filter the DataFrame for selected countries
    filtered_df = df[df['Entity'].isin(selected_countries)]

    # Prepare the DataFrame focusing only on Basic Education
    basic_education_df = filtered_df[['Entity', 'Year', 'Share of population (Basic Education)']]
    melted_df = basic_education_df.rename(columns={'Share of population (Basic Education)': 'Basic Education Share'})

    # Create a grouped bar chart
    fig = px.bar(melted_df,
                 x='Year',
                 y='Basic Education Share',
                 color='Entity',
                 barmode='group',
                 title='Share of Population with Basic Education (Selected Countries Over Years)',
                 labels={'Basic Education Share': 'Share of Population (%)', 'Year': 'Year'})

    # Update layout for better readability
    fig.update_layout(yaxis_title="Share of Population (%)",
                      xaxis_title="Year",
                      legend_title="Country")

    # Convert the figure to HTML for rendering in the template
    graph = fig.to_html()

    # Render the template and pass the graph to the context
    return render(request, 'EduPop4.html', {'graph': graph})

def EduPop5(request):
    # Load your dataset inside the function
    data = pd.read_csv("Global Education (World Population).csv")
    df = pd.DataFrame(data)

    # Select 10 specific countries
    selected_countries = ["India", "Brazil", "Algeria", "Albania",
                          "Afghanistan", "Zimbabwe", "Zambia",
                          "Mexico", "Spain", "Germany", "Australia"]

    # Filter the DataFrame for selected countries
    filtered_df = df[df['Entity'].isin(selected_countries)]

    # Prepare the DataFrame focusing only on No Education
    no_education_df = filtered_df[['Entity', 'Year', 'Share of population (No Education)']]
    melted_df = no_education_df.rename(columns={'Share of population (No Education)': 'No Education Share'})

    # Create a grouped bar chart
    fig = px.bar(melted_df,
                 x='Year',
                 y='No Education Share',
                 color='Entity',
                 barmode='group',
                 title='Share of Population Without Education (Selected Countries Over Years)',
                 labels={'No Education Share': 'Share of Population (%)', 'Year': 'Year'})

    # Update layout for better readability
    fig.update_layout(yaxis_title="Share of Population (%)",
                      xaxis_title="Year",
                      legend_title="Country")

    # Convert the figure to HTML for rendering in the template
    graph = fig.to_html()

    # Render the template and pass the graph to the context
    return render(request, 'EduPop5.html', {'graph': graph})

def EduPop6(request):
    # Load the dataset
    data = pd.read_csv("Global Education (World Population).csv")
    df = pd.DataFrame(data)

    # Select a specific year for analysis
    selected_year = 2020  # Change this to the year you want to analyze

    # Select countries for analysis
    selected_countries = ['Albania', 'Afghanistan', 'Algeria', 'Brazil', 'Canada', 'France', 'India']

    # Filter the data for the selected countries and year
    filtered_data = df[(df['Entity'].isin(selected_countries)) & (df['Year'] == selected_year)]

    # Prepare data for donut chart (Basic Education)
    labels = filtered_data['Entity']
    values = filtered_data['Share of population (Basic Education)']

    # Create a donut chart
    fig = px.pie(names=labels,
                 values=values,
                 title=f'Share of Population with Basic Education in Selected Countries ({selected_year})',
                 hole=0.4)

    # Add the year in the center of the donut chart
    fig.add_annotation(
        text=str(selected_year),
        font=dict(size=30, color="black"),
        showarrow=False,
        align="center",
        x=0.5,
        y=0.5,
    )

    # Update layout for better appearance
    fig.update_traces(textinfo='percent+label')  # Show percentage and label on slices
    fig.update_layout(title_x=0.5)  # Center the title

    # Convert the plot to HTML format
    graph = fig.to_html()

    # Render the template with the generated graph
    return render(request, 'EduPop6.html', {"graph": graph})

def EduIllit1(request):
    # Load the dataset (outside POST block so it runs for both GET and POST requests)
    data = pd.read_csv("Literate And Iliterate.csv")
    df = pd.DataFrame(data)

    # Get the list of unique countries from the dataset for the dropdown
    countries = df['Entity'].unique().tolist()

    # If it's a POST request, process the form data
    if request.method == "POST":
        # Extract form data for country selection
        country1 = request.POST.get("country1_name")
        country2 = request.POST.get("country2_name")

        # Filter data for the selected countries
        filtered_df = df[df['Entity'].isin([country1, country2])]

        # Create an empty figure
        fig = go.Figure()

        # Add a bar for Literacy rates for country1
        fig.add_trace(go.Bar(x=filtered_df[filtered_df['Entity'] == country1]['Year'],
                             y=filtered_df[filtered_df['Entity'] == country1]['Literate'],
                             name=f'{country1} - Literate',
                             marker_color='blue'))

        # Add a bar for Illiteracy rates for country1
        fig.add_trace(go.Bar(x=filtered_df[filtered_df['Entity'] == country1]['Year'],
                             y=filtered_df[filtered_df['Entity'] == country1]['Illiterate'],
                             name=f'{country1} - Illiterate',
                             marker_color='red'))

        # Add a bar for Literacy rates for country2
        fig.add_trace(go.Bar(x=filtered_df[filtered_df['Entity'] == country2]['Year'],
                             y=filtered_df[filtered_df['Entity'] == country2]['Literate'],
                             name=f'{country2} - Literate',
                             marker_color='green'))

        # Add a bar for Illiteracy rates for country2
        fig.add_trace(go.Bar(x=filtered_df[filtered_df['Entity'] == country2]['Year'],
                             y=filtered_df[filtered_df['Entity'] == country2]['Illiterate'],
                             name=f'{country2} - Illiterate',
                             marker_color='orange'))

        # Customize the layout
        fig.update_layout(
            title=f'Literacy and Illiteracy Rates for {country1} and {country2}',
            xaxis_title='Year',
            yaxis_title='Percentage (%)',
            barmode='group',  # Bars will be grouped together
            hovermode='x unified',
            legend_title_text='Country and Category',
            showlegend=True
        )

        # Convert the figure to HTML for rendering in the template
        graph = fig.to_html()

        # Render the template with the generated graph
        return render(request, 'EduIllit1.html', {
            'countries': countries,
            'graph': graph
        })

    # For a GET request, render the form without a graph
    return render(request, 'EduIllit1.html', {
        'countries': countries,
    })

import pandas as pd
import plotly.graph_objs as go
from django.shortcuts import render

def EduIllit2(request):
    # Load the dataset
    data = pd.read_csv("Literate And Iliterate.csv")

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Filter data for Singapore
    filtered_df = df[df['Entity'] == 'Singapore']

    # Create a figure
    fig = go.Figure()

    # Add bars for Literacy rates
    fig.add_trace(go.Bar(
        x=filtered_df['Year'],
        y=filtered_df['Literate'],
        name='Literate',
        marker_color='blue',
        hovertemplate='Country: Singapore<br>Year: %{x}<br>Literate: %{y}%<extra></extra>'
    ))

    # Add bars for Illiteracy rates
    fig.add_trace(go.Bar(
        x=filtered_df['Year'],
        y=filtered_df['Illiterate'],
        name='Illiterate',
        marker_color='red',
        hovertemplate='Country: Singapore<br>Year: %{x}<br>Illiterate: %{y}%<extra></extra>'
    ))

    # Customize the layout
    fig.update_layout(
        title='Literacy and Illiteracy Rates in Singapore (All Years)',
        xaxis_title='Year',
        yaxis_title='Percentage (%)',
        barmode='group',  # Bars will be grouped together
        hovermode='x unified',
        legend_title_text='Status'
    )

    # Convert the figure to HTML for rendering in the template
    graph = fig.to_html()

    # Render the template with the generated graph
    return render(request, 'EduIllit2.html', {'graph': graph})

def EduIllit3(request):
    # Load the dataset
    data = pd.read_csv("Literate And Iliterate.csv")
    
    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Fetch the unique years for the dropdown
    years = df['Year'].drop_duplicates().to_list()

    if request.method == "POST":
        # Get the selected year from the form
        sy = int(request.POST.get("selectyear"))

        # Select countries of interest
        selected_countries = ['Bangladesh', 'Brazil', 'Egypt', 'Mexico', 'Singapore']

        # Filter data for the selected year and selected countries
        recent_data = df[(df['Year'] == sy) & (df['Entity'].isin(selected_countries))]

        # Create a pie chart
        fig = px.pie(recent_data,
                     names='Entity',
                     values='Literate',
                     title=f'Literacy Rates of Selected Countries in {sy}',
                     hover_name='Entity',
                     labels={'Literate': 'Literacy Rate (%)'})

        # Customize the layout with custom colors for each country
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            marker=dict(
                colors=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A'],  # Custom color list for the countries
                line=dict(color='black', width=3)  # Add black borders around the slices
            )
        )

        # Further customize the layout
        fig.update_layout(
            title=dict(
                text=f'Literacy Rates of Selected Countries in {sy}',
                font=dict(size=24, color='#333333'),  # Custom title font
                x=0.5,  # Center title
                xanchor='center'
            ),
            legend_title_text='Countries',
            legend=dict(
                orientation='h',  # Horizontal legend
                yanchor='bottom',
                y=-0.2,
                xanchor='center',
                x=0.5
            ),
            hoverlabel=dict(
                bgcolor="teal",
                font_size=13,
                font_family="Arial",
            ),
            paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
            plot_bgcolor='rgba(0,0,0,0)'    # Transparent plot area
        )

        # Convert the figure to HTML for rendering in the template
        graph = fig.to_html()

        # Render the template with the generated graph and the years for the dropdown
        return render(request, 'EduIllit3.html', {"graph": graph, "year": years})

    else:
        # For a GET request, render the template with only the year options (no graph)
        return render(request, 'EduIllit3.html', {"year": years})

import pandas as pd
import plotly.express as px
from django.shortcuts import render

def EduIllit4(request):
    # Load the dataset
    data = pd.read_csv("Literate And Iliterate.csv")
    
    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Fetch the unique years for the dropdown
    years = df['Year'].drop_duplicates().to_list()

    if request.method == "POST":
        # Get the selected year from the form
        sy = int(request.POST.get("selectyear"))

        # Select countries of interest
        selected_countries = ['Afghanistan', 'Brazil', 'Egypt', 'Nepal', 'India']

        # Filter data for the selected year and the selected countries
        recent_data = df[(df['Year'] == sy) & (df['Entity'].isin(selected_countries))]

        # Create a donut chart for Illiterate rates (pie chart with a hole)
        fig = px.pie(recent_data,
                     names='Entity',
                     values='Illiterate',
                     title=f'Illiteracy Rates of Selected Countries in {sy}',
                     hover_name='Entity',
                     labels={'Illiterate': 'Illiteracy Rate (%)'})

        # Convert the pie chart to a donut chart by adjusting the hole size
        fig.update_traces(
            hole=0.5,  # Creates the donut hole
            textposition='inside',
            textinfo='percent+label',
            marker=dict(
                colors=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A'],  # Custom color list for the countries
                line=dict(color='black', width=3)  # Add black borders around the slices
            )
        )

        # Further customize the layout
        fig.update_layout(
            title=dict(
                text=f'Illiteracy Rates of Selected Countries in {sy}',
                font=dict(size=24, color='#333333'),  # Custom title font
                x=0.5,  # Center title
                xanchor='center'
            ),
            legend_title_text='Countries',
            legend=dict(
                orientation='h',  # Horizontal legend
                yanchor='bottom',
                y=-0.2,
                xanchor='center',
                x=0.5
            ),
            hoverlabel=dict(
                bgcolor="lightblue",
                font_size=13,
                font_family="Arial"
            ),
            paper_bgcolor='rgba(0,0,0,0)',  # Transparent background
            plot_bgcolor='rgba(0,0,0,0)'    # Transparent plot area
        )

        # Add the year in the center of the donut chart
        fig.add_annotation(
            text=str(sy),  # The text to display (selected year)
            x=0.5, y=0.5,  # Positioning in the center
            font=dict(size=30, color="black"),  # Custom font and color for the year
            showarrow=False
        )

        # Convert the figure to HTML for rendering in the template
        graph = fig.to_html()

        # Render the template with the generated graph and the years for the dropdown
        return render(request, 'EduIllit4.html', {"graph": graph, "year": years})

    else:
        # For a GET request, render the template with only the year options (no graph)
        return render(request, 'EduIllit4.html', {"year": years})


def EduIllit5(request):
    # Load the dataset
    data = pd.read_csv("Literate And Iliterate.csv")

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Select 8 countries for analysis
    selected_countries = [
        'India', 'Brazil', 'Nigeria', 'Bangladesh',
        'Pakistan', 'China', 'South Africa', 'Russia'
    ]

    # Filter the DataFrame for the selected countries
    df_filtered = df[df['Entity'].isin(selected_countries)]

    # Melt the DataFrame for easier plotting
    df_melted = df_filtered.melt(id_vars=["Entity", "Year"], value_vars=["Literate", "Illiterate"],
                                 var_name="Literacy_Status", value_name="Percentage")

    # Find the maximum literate and illiterate rates for each country
    max_rates = df_melted.loc[df_melted.groupby(['Entity', 'Literacy_Status'])['Percentage'].idxmax()]

    # Create a bar plot for highest literate and illiterate rates
    fig = px.bar(max_rates, x="Entity", y="Percentage", color="Literacy_Status",
                 title="Highest Literate and Illiterate Rates for Selected Countries",
                 text="Percentage",
                 barmode='group',
                 hover_data=["Year"])  # Include Year in hover data

    # Show the maximum rates on the bars
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')

    # Update layout for better readability
    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="Percentage",
    )

    # Find the overall maximum value
    overall_max = max_rates.loc[max_rates['Percentage'].idxmax()]

    # Add annotation for the highest value
    fig.add_annotation(
        x=overall_max['Entity'],  # Country with the highest value
        y=overall_max['Percentage'],  # The highest percentage
        text=f"Highest: {overall_max['Percentage']}%",  # Display the highest value
        showarrow=True,
        arrowhead=2,
        ax=0,  # Adjust the position of the annotation
        ay=-40,  # Offset to position the annotation above the bar
        font=dict(size=12, color="black"),
        bgcolor="lightyellow"
    )

    # Convert the figure to HTML for rendering in the template
    graph = fig.to_html()

    # Render the template with the generated graph
    return render(request, 'EduIllit5.html', {'graph': graph})

def EduIllit6(request):
    # Load the dataset
    data = pd.read_csv("Literate And Iliterate.csv")

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Select countries for analysis
    selected_countries = [
        'India', 'Brazil', 'Nigeria', 'Bangladesh',
        'Pakistan', 'China', 'South Africa', 'Russia'
    ]

    # Filter the DataFrame for the selected countries
    df_filtered = df[df['Entity'].isin(selected_countries)]

    # Melt the DataFrame for easier plotting (focusing only on the 'Literate' column)
    df_melted = df_filtered.melt(id_vars=["Entity", "Year"], value_vars=["Literate"],
                                 var_name="Literacy_Status", value_name="Percentage")

    # Calculate the improvement in literacy rates (difference between max and min for each country)
    improvement = df_melted.groupby('Entity')['Percentage'].agg(['max', 'min'])
    improvement['Difference'] = improvement['max'] - improvement['min']
    improvement = improvement.reset_index()

    # Sort by the largest improvement
    improvement_sorted = improvement.sort_values(by='Difference', ascending=False)

    # Create a bar plot for countries with the most significant improvements
    fig = px.bar(improvement_sorted, x='Entity', y='Difference',
                 title="Countries with the Most Significant Improvements in Literacy Rates",
                 text='Difference',
                 color='Difference',
                 color_continuous_scale=px.colors.sequential.Viridis)

    # Show the maximum improvement on the bars
    fig.update_traces(texttemplate='%{text:.2f}', textposition='outside')

    # Update layout for better readability
    fig.update_layout(xaxis_title="Country",
                      yaxis_title="Improvement in Literacy Rate (%)",
                      yaxis_ticksuffix="%")

    # Convert the plot to HTML for rendering in the template
    graph = fig.to_html()

    # Render the template with the generated graph
    return render(request, 'EduIllit6.html', {'graph': graph})


def EduEnrollS1(request):
    # Load dataset
    df = pd.read_csv("School Enrollment (Secondary).csv")

    # Specify the countries you want to select
    selected_countries = ['Argentina', 'Finland', 'World', 'Spain']

    # Filter the DataFrame to include only the selected countries
    df_selected = df[df['Country Name'].isin(selected_countries)]

    # Only keep columns that represent the year (2000-2017) for melting
    # The id_vars include 'Country Name' and we melt the actual year columns only
    year_columns = [str(year) for year in range(2000, 2018)]  # Years as strings
    df_long = df_selected.melt(id_vars=['Country Name'], value_vars=year_columns, var_name='Year', value_name='Enrollment Rate')

    # Ensure 'Year' is treated as an integer type for correct ordering
    df_long['Year'] = df_long['Year'].astype(int)

    # Plot the line chart with enhanced aesthetics
    fig = px.line(df_long, x='Year', y='Enrollment Rate', color='Country Name',
                  title="Secondary School Enrollment Rate",
                  labels={"Enrollment Rate": "Enrollment Rate (%)", "Year": "Year"},
                  markers=True)

    # Customizing the layout for an attractive look
    fig.update_layout(
        title_font=dict(size=24, color='darkblue', family="Arial"),
        xaxis_title='Year',
        yaxis_title='Enrollment Rate (%)',
        legend_title_text='Country',
        plot_bgcolor='rgba(240, 240, 240, 0.8)',  # Light background for better contrast
        font=dict(size=14, family="Verdana"),
        hoverlabel=dict(
            bgcolor="white",
            font_size=13,
            font_family="Verdana"
        ),
        xaxis=dict(
            tickmode='linear',  # Ensure all years are displayed
            tick0=2000,         # Start from the year 2000
            dtick=1             # Display each year as a tick
        )
    )

    # Update traces to smooth the lines and make markers more visible
    fig.update_traces(line=dict(width=3), marker=dict(size=8, symbol='circle'))

    # Customize the x-axis to display all year labels clearly
    fig.update_xaxes(tickangle=-45, showgrid=True, gridwidth=1, gridcolor='LightGray')

    # Customize the y-axis to include grid lines for readability
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')

    # Convert the figure to HTML for rendering in the template
    graph = fig.to_html()

    # Render the template with the generated graph
    return render(request, 'EduEnroll1 (Secondary).html', {'graph': graph})

def EduEnrollS2(request):
    # Load dataset
    df = pd.read_csv("School Enrollment (Secondary).csv")

    # If the request method is POST, get the country name and generate the graph
    if request.method == "POST":
        country_name = request.POST.get("country_name")  # Get the country name from the POST request

        # Filter the DataFrame to include only the selected country
        df_selected = df[df['Country Name'] == country_name]

        # Only keep columns that represent the year (2000-2017) for melting
        year_columns = [str(year) for year in range(2000, 2018)]  # Years as strings
        df_long = df_selected.melt(id_vars=['Country Name'], value_vars=year_columns, var_name='Year', value_name='Enrollment Rate')

        # Ensure 'Year' is treated as an integer type for correct ordering
        df_long['Year'] = df_long['Year'].astype(int)

        # Plot the interactive line chart with vibrant colors
        fig = px.line(df_long, x='Year', y='Enrollment Rate',
                      title=f"Secondary School Enrollment for {country_name}",
                      labels={"Enrollment Rate": "Enrollment Rate (%)", "Year": "Year"},
                      markers=True,
                      color_discrete_sequence=['green'],  # Using green color
                      hover_data=['Country Name'])  # Add Country Name to hover data

        # Customizing the layout for an attractive and interactive look
        fig.update_layout(
            title_font=dict(size=24, color='blue', family="Arial"),
            xaxis_title='Year',
            yaxis_title='Enrollment Rate (%)',
            plot_bgcolor='rgba(240, 240, 240, 0.8)',  # Light background for better contrast
            font=dict(size=14, family="Verdana"),
            hoverlabel=dict(
                bgcolor="yellow",  # Custom background for hover labels
                font_size=13,
                font_family="Verdana"
            ),
            xaxis=dict(
                tickmode='linear',  # Ensure all years are displayed
                tick0=2000,         # Start from the year 2000
                dtick=1             # Display each year as a tick
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor='LightGray',
                zeroline=True,  # Show a line at y=0 for reference
                zerolinecolor='Gray'
            ),
            legend=dict(
                orientation="h",   # Horizontal legend at the bottom
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )

        # Update traces to set the line color and marker properties
        fig.update_traces(
            line=dict(width=4, color='blue'),  # Set the line color to blue
            marker=dict(size=10, symbol='circle', line=dict(width=1, color='green'))  # Larger, outlined markers
        )

        # Customize the x-axis to display all year labels clearly
        fig.update_xaxes(tickangle=-45, showgrid=True, gridwidth=1, gridcolor='gray')

        # Convert the plot to HTML for rendering
        graph = fig.to_html()

        # Prepare the list of countries for the dropdown
        countries = df['Country Name'].drop_duplicates().tolist()

        # Render the template with the graph and country list
        return render(request, 'EduEnroll2 (Secondary).html', {'graph': graph, 'countries': countries})

    else:
        # If not a POST request, render the template without the graph but with the country list
        countries = df['Country Name'].drop_duplicates().tolist()
        return render(request, 'EduEnroll2 (Secondary).html', {'countries': countries})

def EduEnrollS3(request):
    # Load your dataset
    df = pd.read_csv("School Enrollment (Secondary).csv")

    # List of countries and years for the dropdowns
    countries = df['Country Name'].unique().tolist()
    years = list(range(2000, 2017))  # Adjust based on available data

    # If it's a POST request, process the form data
    if request.method == "POST":
        # Extract form data
        country1 = request.POST.get("country1_name")
        country2 = request.POST.get("country2_name")
        start_year = int(request.POST.get("startyear"))
        end_year = int(request.POST.get("endyear"))

        # Function to generate the enrollment comparison plot
        def plot_comparison_enrollment(df, country1, country2, start_year, end_year):
            # Define the list of years based on the start and end years
            years_range = [str(year) for year in range(start_year, end_year + 1)]

            # Filter the DataFrame for the specific countries
            country1_data = df[df['Country Name'] == country1]
            country2_data = df[df['Country Name'] == country2]

            # Melt the data to a long format for both countries
            country1_long = country1_data[['Country Name'] + years_range].melt(id_vars='Country Name', var_name='Year', value_name='Enrollment Rate').assign(Country=country1)
            country2_long = country2_data[['Country Name'] + years_range].melt(id_vars='Country Name', var_name='Year', value_name='Enrollment Rate').assign(Country=country2)

            # Combine the data for both countries
            combined_data = pd.concat([country1_long, country2_long])

            # Create the line plot using Plotly Express
            fig = px.line(
                combined_data,
                x='Year',
                y='Enrollment Rate',
                color='Country',
                title=f'Secondary School Enrollment Rate Comparison: {country1} vs {country2} ({start_year}-{end_year})',
                labels={'Enrollment Rate': 'Enrollment Rate (%)'},
                markers=True
            )

            # Update layout settings for better visualization
            fig.update_layout(
                xaxis_title='Year',
                yaxis_title='Enrollment Rate (%)',
                xaxis=dict(tickvals=[str(year) for year in range(start_year, end_year + 1)], ticktext=years_range),
                yaxis=dict(tickformat=".2f"),
                legend_title_text='Country'
            )

            return fig

        # Generate the plot
        fig = plot_comparison_enrollment(df, country1, country2, start_year, end_year)
        graph = fig.to_html()

        # Render the template with the generated graph
        return render(request, 'EduEnroll3 (Secondary).html', {
            'countries': countries,
            'years': years,
            'graph': graph,
            'selected_country1': country1,
            'selected_country2': country2,
            'start_year': start_year,
            'end_year': end_year
        })

    # For a GET request, render the form without a graph
    return render(request, 'EduEnroll3 (Secondary).html', {
        'countries': countries,
        'years': years
    })

def EduEnrollS4(request):
    # Load the dataset
    file_path = "School Enrollment (Secondary).csv"
    data = pd.read_csv(file_path)

    # Extract all the years dynamically from the dataset columns (excluding 'Country Name')
    years = [col for col in data.columns if col.isdigit()]

    # List of selected countries for the chart (can be modified)
    selected_countries = ['Argentina', 'Belgium', 'Bulgaria', 'Bolivia', 'Arab World', 'Brazil', 'World']

    if request.method == "POST":
        # Extract form data for the selected start year and end year
        start_year = int(request.POST.get("startyear"))
        end_year = int(request.POST.get("endyear"))

        # Define the list of years based on the selected range
        selected_years = [str(year) for year in range(start_year, end_year + 1)]

        # Melt the DataFrame to have years as a single column
        data_melted = data.melt(id_vars=['Country Name'],
                                value_vars=selected_years,
                                var_name='Year',
                                value_name='Secondary School Enrollment Rate (%)')

        # Filter the melted DataFrame for the selected countries
        data_filtered = data_melted[data_melted['Country Name'].isin(selected_countries)]

        # Create a bar chart to visualize the data using Plotly
        fig = go.Figure()

        # Add bars for each selected country
        for country in selected_countries:
            country_data = data_filtered[data_filtered['Country Name'] == country]
            fig.add_trace(go.Bar(
                x=country_data['Year'],
                y=country_data['Secondary School Enrollment Rate (%)'],
                name=country,
                textposition='none',  # No text displayed on the bars
                hoverinfo='text',  # Show text on hover
                hovertemplate=f'Country: {country}<br>Year: %{{x}}<br>Enrollment Rate: %{{y:.2f}}%<extra></extra>'  # Custom hover template
            ))

        # Update layout for better presentation
        fig.update_layout(
            title=f'Secondary School Enrollment Rates for Selected Countries ({start_year}-{end_year})',
            xaxis_title='Year',
            yaxis_title='Enrollment Rate (%)',
            barmode='group',  # Group bars by country
            yaxis=dict(range=[0, 100]),  # Adjust y-axis range as necessary
            legend_title='Country',
            xaxis_tickangle=-45  # Rotate x-axis labels for better visibility
        )

        # Convert the plot to HTML
        graph = fig.to_html()

        # Render the template with the graph and the list of available years
        return render(request, 'EduEnroll4 (Secondary).html', {
            "graph": graph,
            "years": years,
            "selected_start_year": start_year,
            "selected_end_year": end_year
        })

    # For a GET request, render the form with the years dropdown and no graph
    return render(request, 'EduEnroll4 (Secondary).html', {
        "years": years
    })


def EduEnrollS5(request):
    if request.method == "POST":
        # Get the selected year from the form
        sy = int(request.POST.get("selectyear"))

        # Load the dataset
        Dataset = pd.read_csv("School Enrollment (Secondary).csv")

        # Define a function to plot the top enrollment countries as a donut chart
        def plot_top_enrollment_countries_donut(df, year, top_n=10):
            # Melt the DataFrame to long format
            df_melted = df.melt(id_vars=['Country Name'],
                                value_vars=[str(y) for y in range(2000, 2018)],  # Adjust the range according to your data
                                var_name='Year',
                                value_name='Enrollment Rate')

            # Convert the Year column to numeric
            df_melted['Year'] = pd.to_numeric(df_melted['Year'], errors='coerce')

            # Filter the DataFrame for the specified year and drop rows with NaN Enrollment Rate
            df_year = df_melted[df_melted['Year'] == year].dropna(subset=['Enrollment Rate'])

            # Sort the countries by enrollment rate and select the top N countries
            top_countries = df_year.nlargest(top_n, 'Enrollment Rate')

            # Create the donut chart
            fig = px.pie(
                top_countries,
                names='Country Name',
                values='Enrollment Rate',
                title=f'Top {top_n} Countries by Secondary School Enrollment Rate in {year}',
                labels={'Enrollment Rate': 'Enrollment Rate (%)'},
                hole=0.3  # Create a donut-style pie chart
            )

            # Customize the layout for clarity
            fig.update_traces(textinfo='percent+label')  # Show percentage and label on the pie slices
            fig.update_layout(
                height=600,  # Adjust height for better spacing
                margin=dict(l=50, r=50, t=50, b=50)  # Adjust margins for better spacing
            )

            # Add only the year in the center of the donut chart
            fig.add_annotation(
                text=str(year),  # Only the year
                showarrow=False,
                font=dict(size=28, color="black"),  # Font size and color
                x=0.5, y=0.5,  # Center position
                align="center",
                bgcolor="rgba(255, 255, 255, 0)",  # Transparent background
            )

            return fig

        # Plot for the selected year
        fig = plot_top_enrollment_countries_donut(Dataset, sy, top_n=10)

        if fig:  # Check if a figure was created
            # Convert the figure to HTML for rendering in the template
            graph = fig.to_html()

            # Fetch the unique years for the dropdown
            years = [col for col in Dataset.columns if col.isdigit()]  # Extract years from column names

            # Render the template with the graph and years
            return render(request, 'EduEnroll5 (Secondary).html', {"graph": graph, "year": years})

    else:
        # Load the dataset to get the list of years
        Dataset = pd.read_csv("School Enrollment (Secondary).csv")

        # Fetch the unique years for the dropdown (filter column names that are years)
        years = [col for col in Dataset.columns if col.isdigit()]

        # Render the template with the year options (no graph)
        return render(request, 'EduEnroll5 (Secondary).html', {"year": years})

def EduEnrollS6(request):
    # Load the dataset into a DataFrame
    df = pd.read_csv("School Enrollment (Secondary).csv")

    # Select specific countries for the analysis
    selected_countries = ["Argentina", "Belgium", "Bolivia",'Arab World', 'Brazil', 'World']

    # Filter the DataFrame for the selected countries
    df_filtered = df[df["Country Name"].isin(selected_countries)]

    # Reshape the filtered DataFrame to a long format for Plotly Express
    df_long = pd.melt(df_filtered, id_vars=["Country Name"],
                      value_vars=[str(year) for year in range(2000, 2018)],
                      var_name="Year", value_name="Enrollment Rate")

    # Convert the Year column to numeric
    df_long["Year"] = pd.to_numeric(df_long["Year"])

    # Find the maximum enrollment rate
    max_row = df_long.loc[df_long["Enrollment Rate"].idxmax()]
    max_rate = max_row["Enrollment Rate"]
    max_country = max_row["Country Name"]
    max_year = max_row["Year"]

    # Create a bar chart using Plotly Express for the selected countries
    fig = px.bar(df_long, x="Year", y="Enrollment Rate", color="Country Name",
                 title="Secondary School Enrollment Rates",
                 labels={"Enrollment Rate": "Secondary School Enrollment (% Net)"},
                 barmode='group')  # Grouped bars by year and country

    # Customize the layout
    fig.update_layout(legend_title_text='Country',
                      xaxis_title='Year',
                      yaxis_title='Enrollment Rate (%)')

    # Add an annotation for the highest enrollment rate
    fig.add_annotation(x=max_year, y=max_rate,
                       text=f"Highest: {max_country} ({max_rate:.2f}%)",
                       showarrow=True, arrowhead=2, ax=-30, ay=-40)

    # Convert the plot to HTML for rendering in the template
    graph = fig.to_html()

    # Render the template with the graph
    return render(request, 'EduEnroll6 (Secondary).html', {'graph': graph})


def EduPrediction1(request):
     if request.method=='POST':
          df=pd.read_csv("Education GDP.csv",parse_dates=['Year'])
          df.dtypes
          country=request.POST.get('country')
         
          print(country)
          #country='India'
          production=df[df['Entity']==country]
          production=production.loc[:,['Year','Expenditure GDP']]
          production=production.sort_values('Year')
          production.isnull().sum()
          production=production.set_index('Year')
          production.index
          y=production
          p = d = q = range(0, 2)
          pdq = list(itertools.product(p, d, q))
          seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
          print('Examples of parameter combinations for Seasonal ARIMA...')
          print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
          print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
          print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
          print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))

          min=99999999
          p1=[-1,-1,-1]
          p2=[-1,-1,-1,-1]
          for param in pdq:
               for param_seasonal in seasonal_pdq:
                    try:
                         mod = sm.tsa.statespace.SARIMAX(y,
                                                       order=param,
                                                       seasonal_order=param_seasonal,
                                                       enforce_stationarity=False,
                                                       enforce_invertibility=False)
                         results = mod.fit()
                         if results.aic<min:
                              min=results.aic
                              p1=param
                              p2=param_seasonal
                         print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
                    except:
                         continue
          print(p1)
          print(min)
          print(p2)
          # 12 is the interval for 12 months
          mod = sm.tsa.statespace.SARIMAX(y,
                                        order=(p1[0], p1[1], p1[2]),
                                        seasonal_order=(p2[0], p2[1], p2[2], 12),
                                        enforce_stationarity=False,
                                        enforce_invertibility=False)
          results = mod.fit()
          print(results.summary().tables[1])
          steps = int(request.POST.get('steps'))
         
          print("steps are",steps)
          pred_uc = results.get_forecast(steps=steps)
               # Create traces
          fig = go.Figure()
          fig.add_trace(go.Scatter(x=y.index, y=y['Expenditure GDP'],
                              mode='lines',
                              name='Actual Value',fill='tozeroy'))
          type(pred_uc.predicted_mean)
          fig.add_trace(go.Scatter(x=pred_uc.predicted_mean.index, y=pred_uc.predicted_mean,
                              mode='lines',
                              name='Predicted Value',fill='tozeroy'))
          #fig.show()
          fig.update_layout(
          title="Education Expenditure GDP by "+ country,
          xaxis_title="Year",
          yaxis_title="Expenditure (% of GDP)",
          legend_title="Values",plot_bgcolor= "lightsteelblue",
          height=500,
          width=1000,
          #paper_bgcolor="#f8b28b",
          title_font_size=20,
          font=dict(family="Verdana",size=18,color="black"), title_x=0.5,
          xaxis_title_font_size=18,yaxis_title_font_size=18, xaxis = dict(showgrid=True, showline=True,gridcolor="Lightgray", linecolor="black"),
          yaxis=dict(showgrid=True, gridcolor="Lightgray", showline=True, linecolor="black"))
          graph=fig.to_html()
          data=pd.read_csv("Education GDP.csv")
          ce=["Algeria","Antigua and Barbuda","Aruba","Botswana", "British Virgin Islands","Brunei","Burkina Faso","Cambodia","Cape Verde","Cayman Islands","Central Europe and the Baltics (WB)",
          "Chad","Comoros","Congo","Cuba","Curacao","Democratic Republic of Congo","Djibouti","Dominican Republic","EU","East Asia and the Pacific (WB)","East Timor","Eritrea","Europe and Central Asia (WB)",
          "Europe and Central Asia (WB)", "Grenada", "Guatemala", "Guinea-Bissau","Haiti","High-income countries","India","Ireland","Jordan","Kiribati","Kuwait","Lebanon","Liberia","Liechtenstein","Low-income countries",
          "Lower-middle-income countries","Malawi","Marshall Islands","Mauritania","Micronesia (country)","Middle East and North Africa (WB)","Monaco","Morocco","Mozambique","Myanmar","Nauru","New Zealand","Nicaragua","Oman",
          "Pakistan","Palestine","Panama","Papua New Guinea","Peru","Philippines","Poland","Puerto Rico","San Marino","Saudi Arabia","Serbia","Slovenia","Solomon Islands","Somalia","South Africa","South Asia (WB)","South Korea",
          "South Sudan","Southern and Eastern Africa (WB)","Sri Lanka","Sub-Saharan Africa (WB)","Sudan","Suriname","Sweden","Syria","Togo","Tonga","Turkmenistan","Turks and Caicos Islands","Uganda","Vanuatu","Venezuela","Western and Central Africa (WB)",
          "Zambia","Zimbabwe"]
          data=data[~data["Entity"].isin(ce)]
          column=data["Entity"].drop_duplicates().tolist()
          user=Register_model.objects.get(Email=request.session['em'])    
          return render(request,'EduPrediction1.html',{'graph':graph,"data":column,"user":user})

     
     else:
          data=pd.read_csv("Education GDP.csv")
          data=pd.read_csv("Education GDP.csv")
          ce=["Algeria","Antigua and Barbuda","Aruba","Botswana", "British Virgin Islands","Brunei","Burkina Faso","Cambodia","Cape Verde","Cayman Islands","Central Europe and the Baltics (WB)",
          "Chad","Comoros","Congo","Cuba","Curacao","Democratic Republic of Congo","Djibouti","Dominican Republic","EU","East Asia and the Pacific (WB)","East Timor","Eritrea","Europe and Central Asia (WB)",
          "Europe and Central Asia (WB)", "Grenada", "Guatemala", "Guinea-Bissau","Haiti","High-income countries","India","Ireland","Jordan","Kiribati","Kuwait","Lebanon","Liberia","Liechtenstein","Low-income countries",
          "Lower-middle-income countries","Malawi","Marshall Islands","Mauritania","Micronesia (country)","Middle East and North Africa (WB)","Monaco","Morocco","Mozambique","Myanmar","Nauru","New Zealand","Nicaragua","Oman",
          "Pakistan","Palestine","Panama","Papua New Guinea","Peru","Philippines","Poland","Puerto Rico","San Marino","Saudi Arabia","Serbia","Slovenia","Solomon Islands","Somalia","South Africa","South Asia (WB)","South Korea",
          "South Sudan","Southern and Eastern Africa (WB)","Sri Lanka","Sub-Saharan Africa (WB)","Sudan","Suriname","Sweden","Syria","Togo","Tonga","Turkmenistan","Turks and Caicos Islands","Uganda","Vanuatu","Venezuela","Western and Central Africa (WB)",
          "Zambia","Zimbabwe"]
          data=data[~data["Entity"].isin(ce)]
          column=data["Entity"].drop_duplicates().tolist()
          user=Register_model.objects.get(Email=request.session['em'])    
          return render(request,'EduPrediction1.html',{"data":column,"user":user})


# from django.shortcuts import render
# import pandas as pd
# import warnings
# import itertools
# import numpy as np
# import statsmodels.api as sm
# import plotly.graph_objects as go

# def EduPrediction2(request):
#     if request.method == "POST":
#         # Get user inputs
#         country = request.POST.get("country")
#         steps = int(request.POST.get("steps"))  # Number of steps for prediction

#         # Load and preprocess dataset
#         df = pd.read_csv('literacyratemale.csv')
#         df = df.transpose()
#         df.columns = df.iloc[0, :]
#         df = df.iloc[4:, :]
        
#         # Convert data to appropriate types
#         c = dict.fromkeys(df.columns, float)
#         df = df.astype(c).reset_index()
#         df.rename(columns={"index": "Year"}, inplace=True)

#         # Filter data for the selected country
#         rate = df.loc[:, ['Year', country]]
#         rate['Year'] = pd.to_datetime(rate['Year'], format='%Y')
#         rate = rate.sort_values('Year').set_index('Year')
        
#         # Model training with SARIMAX
#         p = d = q = range(0, 3)
#         pdq = list(itertools.product(p, d, q))
#         seasonal_pdq = [(x[0], x[1], x[2], 12) for x in itertools.product(p, d, q)]

#         # Search for the best model parameters based on AIC
#         min_aic = float('inf')
#         best_pdq = None
#         best_seasonal_pdq = None

#         for param in pdq:
#             for param_seasonal in seasonal_pdq:
#                 try:
#                     model = sm.tsa.statespace.SARIMAX(
#                         rate,
#                         order=param,
#                         seasonal_order=param_seasonal,
#                         enforce_stationarity=False,
#                         enforce_invertibility=False
#                     )
#                     results = model.fit()
#                     if results.aic < min_aic:
#                         min_aic = results.aic
#                         best_pdq = param
#                         best_seasonal_pdq = param_seasonal
#                 except:
#                     continue

#         # Train the best model
#         model = sm.tsa.statespace.SARIMAX(
#             rate,
#             order=best_pdq,
#             seasonal_order=best_seasonal_pdq,
#             enforce_stationarity=False,
#             enforce_invertibility=False
#         )
#         results = model.fit()

#         # Generate predictions
#         pred_uc = results.get_forecast(steps=steps)

#         # Visualization
#         fig = go.Figure()
#         fig.add_trace(go.Scatter(x=rate.index, y=rate[country], mode='lines', name='Actual Value'))
#         fig.add_trace(go.Scatter(x=pred_uc.predicted_mean.index, y=pred_uc.predicted_mean, mode='lines', name='Predicted Value'))

#         graph = fig.to_html()

#         return render(request, "EduPrediction2.html", {
#             'graph': graph,
#             'title': "Prediction on Male Literacy Rate",
#             'data': df.columns[1:]  # Dropdown options (country names)
#         })

#     else:
#         # Load the dataset for dropdown options
#         df = pd.read_csv('literacyratemale.csv')
#         df = df.transpose()
#         data = df.iloc[0, :].to_list()[1:]  # List of countries

#         return render(request, "EduPrediction2.html", {
#             'data': data
#         })


def EduPrediction2(request):
    if request.method == 'POST':
        df = pd.read_csv("Literacy_Rate.csv", parse_dates=['Year'])
        df.dtypes
        country = request.POST.get('country')

        print(country)
        # country = 'India'
        production = df[df['Entity'] == country]
        production = production.loc[:, ['Year', 'Literacy Rate']]
        production = production.sort_values('Year')
        production.isnull().sum()
        production = production.set_index('Year')
        production.index
        y = production
        p = d = q = range(0, 2)
        pdq = list(itertools.product(p, d, q))
        seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

        print('Examples of parameter combinations for Seasonal ARIMA...')
        print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
        print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
        print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
        print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))

        min = 99999999
        p1 = [-1, -1, -1]
        p2 = [-1, -1, -1, -1]

        for param in pdq:
            for param_seasonal in seasonal_pdq:
                try:
                    mod = sm.tsa.statespace.SARIMAX(
                        y,
                        order=param,
                        seasonal_order=param_seasonal,
                        enforce_stationarity=False,
                        enforce_invertibility=False
                    )
                    results = mod.fit()
                    if results.aic < min:
                        min = results.aic
                        p1 = param
                        p2 = param_seasonal
                    print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
                except:
                    continue

        print(p1)
        print(min)
        print(p2)

        # 12 is the interval for 12 months
        mod = sm.tsa.statespace.SARIMAX(
            y,
            order=(p1[0], p1[1], p1[2]),
            seasonal_order=(p2[0], p2[1], p2[2], 12),
            enforce_stationarity=False,
            enforce_invertibility=False
        )
        results = mod.fit()
        print(results.summary().tables[1])

        steps = int(request.POST.get('steps'))

        print("steps are", steps)
        pred_uc = results.get_forecast(steps=steps)

        # Create traces
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=y.index,
            y=y['Literacy Rate'],
            mode='lines',
            name='Actual Value',
            fill='tozeroy'
        ))
        fig.add_trace(go.Scatter(
            x=pred_uc.predicted_mean.index,
            y=pred_uc.predicted_mean,
            mode='lines',
            name='Predicted Value',
            fill='tozeroy'
        ))

        fig.update_layout(
            title="Literacy Rate by " + country,
            xaxis_title="Year",
            yaxis_title="Literacy Rate",
            legend_title="Values",
            plot_bgcolor="lightsteelblue",
            height=500,
            width=1000,
            title_font_size=20,
            font=dict(family="Verdana", size=18, color="black"),
            title_x=0.5,
            xaxis_title_font_size=18,
            yaxis_title_font_size=18,
            xaxis=dict(
                showgrid=True,
                showline=True,
                tickformat='%Y',  # This ensures the x-axis shows only the year.
                gridcolor="Lightgray",
                linecolor="black"
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="Lightgray",
                showline=True,
                linecolor="black"
            )
        )

        graph = fig.to_html()
        data = pd.read_csv("literacyyouth2.csv")
        column = data["Country Name"].drop_duplicates().tolist()
        user = Register_model.objects.get(Email=request.session['em'])
        return render(request, 'EduPrediction2.html', {'graph': graph, "data": column, "user": user})

    else:
        data = pd.read_csv("literacyyouth2.csv")
        column = data["Country Name"].drop_duplicates().tolist()
        user = Register_model.objects.get(Email=request.session['em'])
        return render(request, 'EduPrediction2.html', {"data": column, "user": user})



def EduPrediction3(request):
     if request.method=='POST':
          df=pd.read_csv("School Enrollment (Primary).csv")
          df=df.transpose()
          df.columns=df.iloc[0,:]
          df=df.iloc[4:,:]
          c=dict.fromkeys(df.columns,float)
          df=df.astype(c)
          print(df.dtypes)
          df=df.reset_index()
          df.rename(columns={"index":"Year"},inplace=True)
          df["Year"]=pd.to_datetime(df["Year"])
          country=request.POST.get('country')
         
          print(country)
          #country='India'
          df=df.loc[:,["Year",country]]
          df=df.sort_values('Year')
          df.isnull().sum()
          production=df.set_index('Year')
          production.index
          y=production
          p = d = q = range(0, 3)
          pdq = list(itertools.product(p, d, q))
          seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
          print('Examples of parameter combinations for Seasonal ARIMA...')
          print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
          print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
          print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
          print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))

          min=99999999
          p1=[-1,-1,-1]
          p2=[-1,-1,-1,-1]
          for param in pdq:
               for param_seasonal in seasonal_pdq:
                    try:
                         mod = sm.tsa.statespace.SARIMAX(y,
                                                       order=param,
                                                       seasonal_order=param_seasonal,
                                                       enforce_stationarity=False,
                                                       enforce_invertibility=False)
                         results = mod.fit()
                         if results.aic<min:
                              min=results.aic
                              p1=param
                              p2=param_seasonal
                         print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
                    except:
                         continue
          print(p1)
          print(min)
          print(p2)
          # 12 is the interval for 12 months
          mod = sm.tsa.statespace.SARIMAX(y,
                                        order=(p1[0], p1[1], p1[2]),
                                        seasonal_order=(p2[0], p2[1], p2[2], 12),
                                        enforce_stationarity=False,
                                        enforce_invertibility=False)
          results = mod.fit()
          print(results.summary().tables[1])
          steps = int(request.POST.get('steps'))
         
          print("steps are",steps)
          pred_uc = results.get_forecast(steps=steps)
               # Create traces
          fig = go.Figure()
          fig.add_trace(go.Scatter(x=y.index, y=y[country],
                              mode='lines',
                              name='Actual Value',fill='tozeroy'))
          type(pred_uc.predicted_mean)
          fig.add_trace(go.Scatter(x=pred_uc.predicted_mean.index, y=pred_uc.predicted_mean,
                              mode='lines',
                              name='Predicted Value',fill='tozeroy'))
          #fig.show()
          fig.update_layout(
          title="Primary School Enrollment Rate by "+ country,
          xaxis_title="Year",
          yaxis_title="School Enrollment Rate",
          legend_title="Values",plot_bgcolor= "lightsteelblue",
          height=500,
          width=1000,
          #paper_bgcolor="#f8b28b",
          title_font_size=20,
          font=dict(family="Verdana",size=18,color="black"), title_x=0.5,
          xaxis_title_font_size=18,yaxis_title_font_size=18, xaxis = dict(showgrid=True, showline=True,gridcolor="Lightgray", linecolor="black"),
          yaxis=dict(showgrid=True, gridcolor="Lightgray", showline=True, linecolor="black"))
          graph=fig.to_html()
          data=pd.read_csv("School Enrollment (Primary).csv")
          ce=["Argentina","Azerbaijan","Burkina Faso","Cyprus","Algeria","Europe & Central Asia","Ecuador",
          "Euro area","Eritrea","Spain","United Kingdom","Ghana","Guinea","IBRD only","IDA only","India","Iceland","Turkiye","Lesotho","Lithuania","Macao SAR","Morocco","Montenegro","Mozambique","Netherlands","Peru","Poland""Slovenia","Sweden","East Asia & Pacific (IDA & IBRD countries)"]
          data=data[~data["Country Name"].isin(ce)]
          column=data["Country Name"].drop_duplicates().tolist()
          user=Register_model.objects.get(Email=request.session['em']) 
          return render(request,'EduPrediction3.html',{'graph':graph,"data":column,"user":user})

     
     else:
          data=pd.read_csv("School Enrollment (Primary).csv")
          ce=["Argentina","Azerbaijan","Burkina Faso","Cyprus","Algeria","Europe & Central Asia","Ecuador",
          "Euro area","Eritrea","Spain","United Kingdom","Ghana","Guinea","IBRD only","IDA only","India","Iceland","Turkiye","Lesotho","Lithuania","Macao SAR","Morocco","Montenegro","Mozambique","Netherlands","Peru","Poland""Slovenia","Sweden","East Asia & Pacific (IDA & IBRD countries)"]
          data=data[~data["Country Name"].isin(ce)]
          column=data["Country Name"].drop_duplicates().tolist()
          user=Register_model.objects.get(Email=request.session['em'])    
          return render(request,'EduPrediction3.html',{"data":column,"user":user})



def EduPredict4(request):
	user=Register_model.objects.get(Email=request.session['em'])
	return render(request,'EduPredict4.html',{'user':user})

def EduPrediction4(request):
    if request.method == 'POST':
        # Read the dataset
        df = pd.read_csv("Global Education (World Population).csv", parse_dates=['Year'])
        
        # Get the country from the POST request
        country = request.POST.get('country')
        print(country)
        
        # Filter the dataset for the selected country
        production = df[df['Entity'] == country]
        production = production.loc[:, ['Year','Share of population (Basic Education)']]
        production = production.sort_values('Year')
        production = production.set_index('Year')

        # Separate the columns
        basic_education = production[['Share of population (Basic Education)']]

        # Define SARIMA parameters
        p = d = q = range(0, 2)  # Ensure 'd' is non-negative
        pdq = list(itertools.product(p, d, q))
        seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
        print('Examples of parameter combinations for Seasonal ARIMA...')
        print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
        print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
        print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
        print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))

        # Helper function to find the best SARIMA model based on AIC
        def find_best_sarima(data):
            min_aic = float('inf')
            best_pdq = None
            best_seasonal_pdq = None
            for param in pdq:
                for param_seasonal in seasonal_pdq:
                    try:
                        mod = sm.tsa.statespace.SARIMAX(data,
                                                        order=param,
                                                        seasonal_order=param_seasonal,
                                                        enforce_stationarity=False,
                                                        enforce_invertibility=False)
                        results = mod.fit()
                        if results.aic < min_aic:
                            min_aic = results.aic
                            best_pdq = param
                            best_seasonal_pdq = param_seasonal
                        print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
                    except:
                        continue
            return best_pdq, best_seasonal_pdq, min_aic


        # Find the best SARIMA model for 'Basic Education'
        best_pdq_basic_education, best_seasonal_pdq_basic_education, min_aic_basic_education = find_best_sarima(basic_education)
        print('Best ARIMA{}x{}12 for Basic Education - AIC:{}'.format(best_pdq_basic_education, best_seasonal_pdq_basic_education, min_aic_basic_education))

        # Fit SARIMA model for 'Basic Education'
        mod_basic_education = sm.tsa.statespace.SARIMAX(basic_education,
                                                        order=best_pdq_basic_education,
                                                        seasonal_order=best_seasonal_pdq_basic_education,
                                                        enforce_stationarity=False,
                                                        enforce_invertibility=False)
        results_basic_education = mod_basic_education.fit()

        # Get the number of steps for forecasting
        steps = int(request.POST.get('steps'))
        print("steps are", steps)

        # Forecast for 'Basic Education'
        pred_basic_education = results_basic_education.get_forecast(steps=steps)

        # Create the plot using Plotly
        fig = go.Figure()

        # Plot actual values for 'Basic Education'
        fig.add_trace(go.Scatter(x=production.index, y=production['Share of population (Basic Education)'],
                                 mode='lines', name='Basic Education', fill='tozeroy'))

        # Plot forecasted values for 'Basic Education'
        fig.add_trace(go.Scatter(x=pred_basic_education.predicted_mean.index, y=pred_basic_education.predicted_mean,
                                 mode='lines', name='Predicted Basic Education', fill='tozeroy'))

        # Update plot layout
        fig.update_layout(
            title=f"Basic Education Share Prediction for {country}",
            xaxis_title="Year",
            yaxis_title="Share of Population (Basic Education)",
            legend_title="Education Level",
            plot_bgcolor="lightsteelblue",
            height=500,
            width=1000,
            title_font_size=20,
            font=dict(family="Verdana", size=18, color="black"),
            title_x=0.5,
            xaxis_title_font_size=18,
            yaxis_title_font_size=18,
            xaxis=dict(showgrid=True, showline=True, gridcolor="Lightgray", linecolor="black"),
            yaxis=dict(showgrid=True, gridcolor="Lightgray", showline=True, linecolor="black")
        )

        # Render the plot
        graph = fig.to_html()
        data = pd.read_csv("Global Education (World Population).csv")
        ce=["Afghanistan","Angola","Antigua and Barbuda","Barbados","Botswana","Brunei","Cameroon","Cape Verde","Chad","China","Curacao",
        "Djibouti","Eastern Europe (OECD)","Eritrea","Fiji","French Guiana","Ghana","Grenada","Guadeloupe","Guam","Guinea","Guinea-Bissau","Kenya","Kiribati","Kuwait",
        "Laos","Latvia","Liberia","Libya","Luxembourg","Madagascar","Martinique","Mauritania","Micronesia (country)","Mozambique","Myanmar","Niger","North Korea","Oman",
        "Palestine","Papua New Guinea","Reunion","Rwanda","Seychelles","Sierra Leone","Solomon Islands","South Sudan","Sri Lanka","Sudan","Taiwan","Togo","Turkey","Uganda",
        "United Arab Emirates","United States Virgin Islands","Uzbekistan","Western Sahara","World","Zimbabwe","Yemen"]
        data=data[~data["Entity"].isin(ce)]
        column = data["Entity"].drop_duplicates().tolist()
        user = Register_model.objects.get(Email=request.session['em'])    
        return render(request, 'EduPrediction4.html', {'graph': graph, "data": column, "user": user})

    else:
        data = pd.read_csv("Global Education (World Population).csv")
        ce=["Afghanistan","Angola","Antigua and Barbuda","Barbados","Botswana","Brunei","Cameroon","Cape Verde","Chad","China","Curacao",
        "Djibouti","Eastern Europe (OECD)","Eritrea","Fiji","French Guiana","Ghana","Grenada","Guadeloupe","Guam","Guinea","Guinea-Bissau","Kenya","Kiribati","Kuwait",
        "Laos","Latvia","Liberia","Libya","Luxembourg","Madagascar","Martinique","Mauritania","Micronesia (country)","Mozambique","Myanmar","Niger","North Korea","Oman",
        "Palestine","Papua New Guinea","Reunion","Rwanda","Seychelles","Sierra Leone","Solomon Islands","South Sudan","Sri Lanka","Sudan","Taiwan","Togo","Turkey","Uganda",
        "United Arab Emirates","United States Virgin Islands","Uzbekistan","Western Sahara","World","Zimbabwe","Yemen"]
        data=data[~data["Entity"].isin(ce)]
        column = data["Entity"].drop_duplicates().tolist()
        user = Register_model.objects.get(Email=request.session['em'])    
        return render(request, 'EduPrediction4.html', {"data": column, "user": user})

def EduPrediction41(request):
    if request.method == 'POST':
        # Read the dataset
        df = pd.read_csv("Global Education (World Population).csv", parse_dates=['Year'])
        
        # Get the country from the POST request
        country = request.POST.get('country')
        print(country)
        
        # Filter the dataset for the selected country
        production = df[df['Entity'] == country]
        production = production.loc[:, ['Year', 'Share of population (No Education)']]
        production = production.sort_values('Year')
        production = production.set_index('Year')

        # Separate the columns
        no_education = production[['Share of population (No Education)']]

        # Define SARIMA parameters
        p = d = q = range(0, 2)  # Ensure 'd' is non-negative
        pdq = list(itertools.product(p, d, q))
        seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
        print('Examples of parameter combinations for Seasonal ARIMA...')
        print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
        print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
        print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
        print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))

        # Helper function to find the best SARIMA model based on AIC
        def find_best_sarima(data):
            min_aic = float('inf')
            best_pdq = None
            best_seasonal_pdq = None
            for param in pdq:
                for param_seasonal in seasonal_pdq:
                    try:
                        mod = sm.tsa.statespace.SARIMAX(data,
                                                        order=param,
                                                        seasonal_order=param_seasonal,
                                                        enforce_stationarity=False,
                                                        enforce_invertibility=False)
                        results = mod.fit()
                        if results.aic < min_aic:
                            min_aic = results.aic
                            best_pdq = param
                            best_seasonal_pdq = param_seasonal
                        print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
                    except:
                        continue
            return best_pdq, best_seasonal_pdq, min_aic

        # Find the best SARIMA model for 'No Education'
        best_pdq_no_education, best_seasonal_pdq_no_education, min_aic_no_education = find_best_sarima(no_education)
        print('Best ARIMA{}x{}12 for No Education - AIC:{}'.format(best_pdq_no_education, best_seasonal_pdq_no_education, min_aic_no_education))

        # Fit SARIMA model for 'No Education'
        mod_no_education = sm.tsa.statespace.SARIMAX(no_education,
                                                     order=best_pdq_no_education,
                                                     seasonal_order=best_seasonal_pdq_no_education,
                                                     enforce_stationarity=False,
                                                     enforce_invertibility=False)
        results_no_education = mod_no_education.fit()

        # Get the number of steps for forecasting
        steps = int(request.POST.get('steps'))
        print("steps are", steps)

        # Forecast for 'No Education'
        pred_no_education = results_no_education.get_forecast(steps=steps)

        # Create the plot using Plotly
        fig = go.Figure()

        # Plot actual values for both 'No Education' and 'Basic Education'
        fig.add_trace(go.Scatter(x=production.index, y=production['Share of population (No Education)'],
                                 mode='lines', name='No Education', fill='tozeroy'))

        # Plot forecasted values for 'No Education'
        fig.add_trace(go.Scatter(x=pred_no_education.predicted_mean.index, y=pred_no_education.predicted_mean,
                                 mode='lines', name='Predicted No Education', fill='tozeroy'))

        # Update plot layout
        fig.update_layout(
            title=f"No Education Share Prediction for {country}",
            xaxis_title="Year",
            yaxis_title="Share of Population (No Education)",
            legend_title="Education Level",
            plot_bgcolor="lightsteelblue",
            height=500,
            width=1000,
            title_font_size=20,
            font=dict(family="Verdana", size=18, color="black"),
            title_x=0.5,
            xaxis_title_font_size=18,
            yaxis_title_font_size=18,
            xaxis=dict(showgrid=True, showline=True, gridcolor="Lightgray", linecolor="black"),
            yaxis=dict(showgrid=True, gridcolor="Lightgray", showline=True, linecolor="black")
        )

        # Render the plot
        graph = fig.to_html()
        data = pd.read_csv("Global Education (World Population).csv")
        ce=["Afghanistan","Angola","Argentina","Austria","Azerbaijan","Bahrain","Barbados","Belarus","Benin","Bosnia and Herzegovina","Botswana","Brazil","Brunei",
        "Bulgaria","Cameroon","Canada","Cape Verde","Chad","Colombia","Curacao","Cyprus","Czechia","Denmark","Djibouti","Dominican Republic","East Asia (OECD)",
        "Eastern Europe (OECD)","Egypt","El Salvador","Equatorial Guinea","Erteria","Estonia","Fiji","Finland","French Guiana","Georgia","Germany","Ghana","Grenada",
        "Guadeloupe","Guam","Guatemala","Guinea","Guinea-Bissau","Iceland","Indonesia","Iran","Ireland","Japan","Jordan","Kazakhstan","Kenya","Kiribati","Kyrgyzstan",
        "Laos","Latin America and Caribbean (OECD)","Latvia","Lesotho","Liberia","Libya","Lithuania","Luxembourg","Madagascar","Malawi","Mali","Martinique","Mauritania",
        "Mauritius","Mexico","Micronesia (country)","Moldova","Mongolia","Montenegro","Morocco","Mozambique","Myanmar","Nepal","Netherlands","New Zealand","Nicaragua","Niger",
        "North Korea","North Macedonia","Norway","Oman","Palestine","Panama","Papua New Guinea","Poland","Portugal","Reunion","Russia","Rwanda","Samoa","Saudi Arabia","Seychelles",
        "Sierra Leone","Slovakia","Slovenia","Solomon Islands","South Korea","South Sudan","South and South-East Asia (OECD)","Sri Lanka","Sub-Sahara Africa (OECD)","Sudan","Suriname",
        "Sweden","Switzerland","Syria","Taiwan","Tajikistan","Thailand","Togo","Tunisia","Turkey","Turkmenistan","Ukraine","United Arab Emirates","United Kingdom","United States Virgin Islands",
        "Uzbekistan","Western Europe (OECD)","Western Offshoots (OECD)","Western Sahara","Yemen","Zambia","Zimbabwe"]
        data=data[~data["Entity"].isin(ce)]
        column = data["Entity"].drop_duplicates().tolist()
        user = Register_model.objects.get(Email=request.session['em'])    
        return render(request, 'EduPrediction4.1.html', {'graph': graph, "data": column, "user": user})

    else:
        data = pd.read_csv("Global Education (World Population).csv")
        ce=["Afghanistan","Angola","Argentina","Austria","Azerbaijan","Bahrain","Barbados","Belarus","Benin","Bosnia and Herzegovina","Botswana","Brazil","Brunei",
        "Bulgaria","Cameroon","Canada","Cape Verde","Chad","Colombia","Curacao","Cyprus","Czechia","Denmark","Djibouti","Dominican Republic","East Asia (OECD)",
        "Eastern Europe (OECD)","Egypt","El Salvador","Equatorial Guinea","Erteria","Estonia","Fiji","Finland","French Guiana","Georgia","Germany","Ghana","Grenada",
        "Guadeloupe","Guam","Guatemala","Guinea","Guinea-Bissau","Iceland","Indonesia","Iran","Ireland","Japan","Jordan","Kazakhstan","Kenya","Kiribati","Kyrgyzstan",
        "Laos","Latin America and Caribbean (OECD)","Latvia","Lesotho","Liberia","Libya","Lithuania","Luxembourg","Madagascar","Malawi","Mali","Martinique","Mauritania",
        "Mauritius","Mexico","Micronesia (country)","Moldova","Mongolia","Montenegro","Morocco","Mozambique","Myanmar","Nepal","Netherlands","New Zealand","Nicaragua","Niger",
        "North Korea","North Macedonia","Norway","Oman","Palestine","Panama","Papua New Guinea","Poland","Portugal","Reunion","Russia","Rwanda","Samoa","Saudi Arabia","Seychelles",
        "Sierra Leone","Slovakia","Slovenia","Solomon Islands","South Korea","South Sudan","South and South-East Asia (OECD)","Sri Lanka","Sub-Sahara Africa (OECD)","Sudan","Suriname",
        "Sweden","Switzerland","Syria","Taiwan","Tajikistan","Thailand","Togo","Tunisia","Turkey","Turkmenistan","Ukraine","United Arab Emirates","United Kingdom","United States Virgin Islands",
        "Uzbekistan","Western Europe (OECD)","Western Offshoots (OECD)","Western Sahara","Yemen","Zambia","Zimbabwe"]
        data=data[~data["Entity"].isin(ce)]
        column = data["Entity"].drop_duplicates().tolist()
        user = Register_model.objects.get(Email=request.session['em'])    
        return render(request, 'EduPrediction4.1.html', {"data": column, "user": user})

def EduPredict5(request):
	user=Register_model.objects.get(Email=request.session['em'])
	return render(request,'EduPredict5.html',{'user':user})

def EduPrediction5(request):
    if request.method == 'POST':
        df = pd.read_csv("Literate And Iliterate.csv", parse_dates=['Year'])
        df.dtypes
        country = request.POST.get('country')

        print(country)
        # Filter the dataframe based on selected country
        production = df[df['Entity'] == country]
        production = production.loc[:, ['Year', 'Literate']]
        production = production.sort_values('Year')
        production.isnull().sum()
        production = production.set_index('Year')
        
        # Choose target variables for prediction
        y_literate = production['Literate']

        # Define p, d, q for ARIMA
        p = d = q = range(0, 2)
        pdq = list(itertools.product(p, d, q))
        seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

        print('Examples of parameter combinations for Seasonal ARIMA...')
        print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
        print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))

        # Define function to find the best model
        def find_best_sarimax(y):
            min_aic = float('inf')
            best_pdq = None
            best_seasonal_pdq = None

            for param in pdq:
                for param_seasonal in seasonal_pdq:
                    try:
                        mod = sm.tsa.statespace.SARIMAX(y,
                                                        order=param,
                                                        seasonal_order=param_seasonal,
                                                        enforce_stationarity=False,
                                                        enforce_invertibility=False)
                        results = mod.fit()
                        if results.aic < min_aic:
                            min_aic = results.aic
                            best_pdq = param
                            best_seasonal_pdq = param_seasonal
                        print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
                    except:
                        continue
            return best_pdq, best_seasonal_pdq

        # Find best models for both Literate and Illiterate rates
        best_pdq_literate, best_seasonal_pdq_literate = find_best_sarimax(y_literate)

        # Fit the final models for Literate and Illiterate rates
        mod_literate = sm.tsa.statespace.SARIMAX(y_literate,
                                                 order=best_pdq_literate,
                                                 seasonal_order=best_seasonal_pdq_literate,
                                                 enforce_stationarity=False,
                                                 enforce_invertibility=False)
        results_literate = mod_literate.fit()

        steps = int(request.POST.get('steps'))
        print("Steps are", steps)

        # Get forecast for Literate and Illiterate
        pred_uc_literate = results_literate.get_forecast(steps=steps)

        # Create traces for the plot
        fig = go.Figure()

        # Plot actual and predicted values for Literate Rate
        fig.add_trace(go.Scatter(x=y_literate.index, y=y_literate,
                                 mode='lines',
                                 name='Actual Literate Value', fill='tozeroy'))
        fig.add_trace(go.Scatter(x=pred_uc_literate.predicted_mean.index, y=pred_uc_literate.predicted_mean,
                                 mode='lines',
                                 name='Predicted Literate Value', fill='tozeroy'))

        # Update layout for the figure
        fig.update_layout(
            title="Literate Rate Prediction for " + country,
            xaxis_title="Year",
            yaxis_title="Literate/Illiterate Rate (Literate)",
            legend_title="Values",
            plot_bgcolor="lightsteelblue",
            height=500,
            width=1000,
            title_font_size=20,
            font=dict(family="Verdana", size=18, color="black"),
            title_x=0.5,
            xaxis_title_font_size=18,
            yaxis_title_font_size=18,
            xaxis=dict(showgrid=True, showline=True, gridcolor="Lightgray", linecolor="black"),
            yaxis=dict(showgrid=True, gridcolor="Lightgray", showline=True, linecolor="black")
        )

        graph = fig.to_html()
        data = pd.read_csv("Literate And Iliterate.csv")
        ce=["Afghanistan","Albania","Algeria","Angola","Armenia","Aruba","Azerbaijan","Belarus","Benin","Bolivia","Bosnia and Herzegovina","Botswana",
        "Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Cape Verde","Cayman Islands","Central African Republic","Chad","Chile","Colombia","Comoros",
        "Congo","Costa Rica","Cote d'Ivoire","Croatia","Cuba","Cyprus","Democratic Republic of Congo","Dominican Republic","East Timor","Egypt","Equatorial Guinea","Eritrea",
        "Estonia","Eswatini","Ethiopia","Guinea-Bissau","Gabon","Gambia","Georgia","Ghana","Greece","Guatemala","Guinea","Guyana","Haiti","Hungary","India","Indonesia","Iran","Iraq","Jordan",
        "Kazakhstan","Kenya","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Lithuania","Madagascar","Malawi","Maldives","Mali","Malta","Marshall Islands","Mauritania",
        "Middle East and North Africa (WB)","Mauritius","Moldova","Montenegro","Morocco","Mozambique","Myanmar","Namibia","Nepal","New Caledonia","Niger","Nigeria","North America (WB)",
        "North Korea","North Macedonia","Oman","Palau","Panama","Papua New Guinea","Peru","Philippines","Poland","Portugal","Puerto Rico","Romania","Rwanda","Samoa","Sao Tome and Principe",
        "Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Somalia","South Korea","South Sudan","Sri Lanka","Sub-Saharan Africa (WB)","Sudan","Suriname","Syria","Tajikistan","Tanzania",
        "Thailand","Togo","Tonga","Tunisia","Uganda","Ukraine","United Arab Emirates","Uzbekistan","Vanuatu","Venezuela","Vietnam","Zambia","Zimbabwe"]
        data=data[~data["Entity"].isin(ce)]
        column = data["Entity"].drop_duplicates().tolist()
        user = Register_model.objects.get(Email=request.session['em'])
        return render(request, 'EduPrediction5.html', {'graph': graph, "data": column, "user": user})

    else:
        data = pd.read_csv("Literate And Iliterate.csv")
        ce=["Afghanistan","Albania","Algeria","Angola","Armenia","Aruba","Azerbaijan","Belarus","Benin","Bolivia","Bosnia and Herzegovina","Botswana",
        "Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Cape Verde","Cayman Islands","Central African Republic","Chad","Chile","Colombia","Comoros",
        "Congo","Costa Rica","Cote d'Ivoire","Croatia","Cuba","Cyprus","Democratic Republic of Congo","Dominican Republic","East Timor","Egypt","Equatorial Guinea","Eritrea",
        "Estonia","Eswatini","Ethiopia","Guinea-Bissau","Gabon","Gambia","Georgia","Ghana","Greece","Guatemala","Guinea","Guyana","Haiti","Hungary","India","Indonesia","Iran","Iraq","Jordan",
        "Kazakhstan","Kenya","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Lithuania","Madagascar","Malawi","Maldives","Mali","Malta","Marshall Islands","Mauritania",
        "Middle East and North Africa (WB)","Mauritius","Moldova","Montenegro","Morocco","Mozambique","Myanmar","Namibia","Nepal","New Caledonia","Niger","Nigeria","North America (WB)",
        "North Korea","North Macedonia","Oman","Palau","Panama","Papua New Guinea","Peru","Philippines","Poland","Portugal","Puerto Rico","Romania","Rwanda","Samoa","Sao Tome and Principe",
        "Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Somalia","South Korea","South Sudan","Sri Lanka","Sub-Saharan Africa (WB)","Sudan","Suriname","Syria","Tajikistan","Tanzania",
        "Thailand","Togo","Tonga","Tunisia","Uganda","Ukraine","United Arab Emirates","Uzbekistan","Vanuatu","Venezuela","Vietnam","Zambia","Zimbabwe"]
        data=data[~data["Entity"].isin(ce)]
        column = data["Entity"].drop_duplicates().tolist()
        user = Register_model.objects.get(Email=request.session['em'])
        return render(request, 'EduPrediction5.html', {"data": column, "user": user})

def EduPrediction51(request):
    if request.method == 'POST':
        df = pd.read_csv("Literate And Iliterate.csv", parse_dates=['Year'])
        df.dtypes
        country = request.POST.get('country')

        print(country)
        # Filter the dataframe based on selected country
        production = df[df['Entity'] == country]
        production = production.loc[:, ['Year', 'Illiterate']]
        production = production.sort_values('Year')
        production.isnull().sum()
        production = production.set_index('Year')
        
        # Choose target variables for prediction
        y_illiterate = production['Illiterate']

        # Define p, d, q for ARIMA
        p = d = q = range(0, 2)
        pdq = list(itertools.product(p, d, q))
        seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]

        print('Examples of parameter combinations for Seasonal ARIMA...')
        print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
        print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))

        # Define function to find the best model
        def find_best_sarimax(y):
            min_aic = float('inf')
            best_pdq = None
            best_seasonal_pdq = None

            for param in pdq:
                for param_seasonal in seasonal_pdq:
                    try:
                        mod = sm.tsa.statespace.SARIMAX(y,
                                                        order=param,
                                                        seasonal_order=param_seasonal,
                                                        enforce_stationarity=False,
                                                        enforce_invertibility=False)
                        results = mod.fit()
                        if results.aic < min_aic:
                            min_aic = results.aic
                            best_pdq = param
                            best_seasonal_pdq = param_seasonal
                        print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
                    except:
                        continue
            return best_pdq, best_seasonal_pdq

        # Find best models for Illiterate rates
        best_pdq_illiterate, best_seasonal_pdq_illiterate = find_best_sarimax(y_illiterate)

        # Fit the final models for Illiterate rates
        mod_illiterate = sm.tsa.statespace.SARIMAX(y_illiterate,
                                                   order=best_pdq_illiterate,
                                                   seasonal_order=best_seasonal_pdq_illiterate,
                                                   enforce_stationarity=False,
                                                   enforce_invertibility=False)
        results_illiterate = mod_illiterate.fit()

        steps = int(request.POST.get('steps'))
        print("Steps are", steps)

        # Get forecast for Illiterate
        pred_uc_illiterate = results_illiterate.get_forecast(steps=steps)

        # Create traces for the plot
        fig = go.Figure()

        # Plot actual and predicted values for Illiterate Rate
        fig.add_trace(go.Scatter(x=y_illiterate.index, y=y_illiterate,
                                 mode='lines',
                                 name='Actual Illiterate Value', fill='tozeroy'))
        fig.add_trace(go.Scatter(x=pred_uc_illiterate.predicted_mean.index, y=pred_uc_illiterate.predicted_mean,
                                 mode='lines',
                                 name='Predicted Illiterate Value', fill='tozeroy'))

        # Update layout for the figure
        fig.update_layout(
            title="Literate and Illiterate Rate Prediction for " + country,
            xaxis_title="Year",
            yaxis_title="Literate/Illiterate Rate (Illiterate)",
            legend_title="Values",
            plot_bgcolor="lightsteelblue",
            height=500,
            width=1000,
            title_font_size=20,
            font=dict(family="Verdana", size=18, color="black"),
            title_x=0.5,
            xaxis_title_font_size=18,
            yaxis_title_font_size=18,
            xaxis=dict(showgrid=True, showline=True, gridcolor="Lightgray", linecolor="black"),
            yaxis=dict(showgrid=True, gridcolor="Lightgray", showline=True, linecolor="black")
        )

        graph = fig.to_html()
        data = pd.read_csv("Literate And Iliterate.csv")
        ce=["Afghanistan","Albania","Algeria","Angola","Armenia","Aruba","Azerbaijan","Bahrain","Belarus","Benin","Bolivia","Bosnia and Herzegovina","Botswana",
        "Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Cape Verde","Cayman Islands","Central African Republic","Chad","Chile","China","Comoros",
        "Congo","Costa Rica","Cote d'Ivoire","Croatia","Cuba","Cyprus","Democratic Republic of Congo","Dominican Republic","East Timor","Egypt","Equatorial Guinea","Eritrea",
        "Estonia","Eswatini","Ethiopia","Guinea-Bissau","Gabon","Gambia","Georgia","Ghana","Greece","Guatemala","Guinea","Guyana","Haiti","Hungary","India","Indonesia","Iran","Iraq","Italy","Jordan",
        "Kazakhstan","Kenya","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Lithuania","Madagascar","Malawi","Maldives","Mali","Malta","Marshall Islands","Mauritania",
        "Middle East and North Africa (WB)","Mauritius","Moldova","Montenegro","Morocco","Mozambique","Myanmar","Namibia","Nepal","New Caledonia","Niger","Nigeria","North America (WB)",
        "North Korea","North Macedonia","Oman","Palau","Panama","Papua New Guinea","Peru","Philippines","Poland","Portugal","Puerto Rico","Romania","Rwanda","Samoa","Sao Tome and Principe",
        "Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Somalia","South Korea","South Sudan","Sri Lanka","Sub-Saharan Africa (WB)","Sudan","Suriname","Syria","Tajikistan","Tanzania",
        "Thailand","Togo","Tonga","Tunisia","Uganda","Ukraine","United Arab Emirates","Uzbekistan","Vanuatu","Venezuela","Vietnam","World","Zambia","Zimbabwe"]
        data=data[~data["Entity"].isin(ce)]
        column = data["Entity"].drop_duplicates().tolist()
        user = Register_model.objects.get(Email=request.session['em'])
        return render(request, 'EduPrediction5.1.html', {'graph': graph, "data": column, "user": user})

    else:
        data = pd.read_csv("Literate And Iliterate.csv")
        ce=["Afghanistan","Albania","Algeria","Angola","Armenia","Aruba","Azerbaijan","Bahrain","Belarus","Benin","Bolivia","Bosnia and Herzegovina","Botswana",
        "Brunei","Bulgaria","Burkina Faso","Burundi","Cambodia","Cameroon","Cape Verde","Cayman Islands","Central African Republic","Chad","Chile","China","Comoros",
        "Congo","Costa Rica","Cote d'Ivoire","Croatia","Cuba","Cyprus","Democratic Republic of Congo","Dominican Republic","East Timor","Egypt","Equatorial Guinea","Eritrea",
        "Estonia","Eswatini","Ethiopia","Guinea-Bissau","Gabon","Gambia","Georgia","Ghana","Greece","Guatemala","Guinea","Guyana","Haiti","Hungary","India","Indonesia","Iran","Iraq","Italy","Jordan",
        "Kazakhstan","Kenya","Kyrgyzstan","Laos","Latvia","Lebanon","Lesotho","Liberia","Lithuania","Madagascar","Malawi","Maldives","Mali","Malta","Marshall Islands","Mauritania",
        "Middle East and North Africa (WB)","Mauritius","Moldova","Montenegro","Morocco","Mozambique","Myanmar","Namibia","Nepal","New Caledonia","Niger","Nigeria","North America (WB)",
        "North Korea","North Macedonia","Oman","Palau","Panama","Papua New Guinea","Peru","Philippines","Poland","Portugal","Puerto Rico","Romania","Rwanda","Samoa","Sao Tome and Principe",
        "Saudi Arabia","Senegal","Serbia","Seychelles","Sierra Leone","Somalia","South Korea","South Sudan","Sri Lanka","Sub-Saharan Africa (WB)","Sudan","Suriname","Syria","Tajikistan","Tanzania",
        "Thailand","Togo","Tonga","Tunisia","Uganda","Ukraine","United Arab Emirates","Uzbekistan","Vanuatu","Venezuela","Vietnam","World","Zambia","Zimbabwe"]
        data=data[~data["Entity"].isin(ce)]
        column = data["Entity"].drop_duplicates().tolist()
        user = Register_model.objects.get(Email=request.session['em'])
        return render(request, 'EduPrediction5.1.html', {"data": column, "user": user})

def EduPrediction6(request):
     if request.method=='POST':
          df=pd.read_csv("School Enrollment (Secondary).csv")
          df=df.transpose()
          df.columns=df.iloc[0,:]
          df=df.iloc[4:,:]
          c=dict.fromkeys(df.columns,float)
          df=df.astype(c)
          print(df.dtypes)
          df=df.reset_index()
          df.rename(columns={"index":"Year"},inplace=True)
          df["Year"]=pd.to_datetime(df["Year"])
          country=request.POST.get('country')
         
          print(country)
          #country='India'
          df=df.loc[:,["Year",country]]
          df=df.sort_values('Year')
          df.isnull().sum()
          production=df.set_index('Year')
          production.index
          y=production
          p = d = q = range(0, 3)
          pdq = list(itertools.product(p, d, q))
          seasonal_pdq = [(x[0], x[1], x[2], 12) for x in list(itertools.product(p, d, q))]
          print('Examples of parameter combinations for Seasonal ARIMA...')
          print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[1]))
          print('SARIMAX: {} x {}'.format(pdq[1], seasonal_pdq[2]))
          print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[3]))
          print('SARIMAX: {} x {}'.format(pdq[2], seasonal_pdq[4]))

          min=99999999
          p1=[-1,-1,-1]
          p2=[-1,-1,-1,-1]
          for param in pdq:
               for param_seasonal in seasonal_pdq:
                    try:
                         mod = sm.tsa.statespace.SARIMAX(y,
                                                       order=param,
                                                       seasonal_order=param_seasonal,
                                                       enforce_stationarity=False,
                                                       enforce_invertibility=False)
                         results = mod.fit()
                         if results.aic<min:
                              min=results.aic
                              p1=param
                              p2=param_seasonal
                         print('ARIMA{}x{}12 - AIC:{}'.format(param, param_seasonal, results.aic))
                    except:
                         continue
          print(p1)
          print(min)
          print(p2)
          # 12 is the interval for 12 months
          mod = sm.tsa.statespace.SARIMAX(y,
                                        order=(p1[0], p1[1], p1[2]),
                                        seasonal_order=(p2[0], p2[1], p2[2], 12),
                                        enforce_stationarity=False,
                                        enforce_invertibility=False)
          results = mod.fit()
          print(results.summary().tables[1])
          steps = int(request.POST.get('steps'))
         
          print("steps are",steps)
          pred_uc = results.get_forecast(steps=steps)
               # Create traces
          fig = go.Figure()
          fig.add_trace(go.Scatter(x=y.index, y=y[country],
                              mode='lines',
                              name='Actual Value',fill='tozeroy'))
          type(pred_uc.predicted_mean)
          fig.add_trace(go.Scatter(x=pred_uc.predicted_mean.index, y=pred_uc.predicted_mean,
                              mode='lines',
                              name='Predicted Value',fill='tozeroy'))
          #fig.show()
          fig.update_layout(
          title="Secondary School Enrollment Rate by "+ country,
          xaxis_title="Year",
          yaxis_title="School Enrollment Rate",
          legend_title="Values",plot_bgcolor= "lightsteelblue",
          height=500,
          width=1000,
          #paper_bgcolor="#f8b28b",
          title_font_size=20,
          font=dict(family="Verdana",size=18,color="black"), title_x=0.5,
          xaxis_title_font_size=18,yaxis_title_font_size=18, xaxis = dict(showgrid=True, showline=True,gridcolor="Lightgray", linecolor="black"),
          yaxis=dict(showgrid=True, gridcolor="Lightgray", showline=True, linecolor="black"))
          graph=fig.to_html()
          data=pd.read_csv("School Enrollment (Secondary).csv")
          ce=["Belgium","Early-demographic dividend","Heavily indebted poor countries (HIPC)","IDA total","IDA blend","Italy","OECD members",
          "Sub-Saharan Africa (excluding high income)","Sub-Saharan Africa","Sub-Saharan Africa (IDA & IBRD countries)","Turkiye"]
          data=data[~data["Country Name"].isin(ce)]
          column=data["Country Name"].drop_duplicates().tolist()
          user=Register_model.objects.get(Email=request.session['em']) 
          return render(request,'EduPrediction6.html',{'graph':graph,"data":column,"user":user})

     
     else:
          data=pd.read_csv("School Enrollment (Secondary).csv")
          ce=["Belgium","Early-demographic dividend","Heavily indebted poor countries (HIPC)","IDA total","IDA blend","Italy","OECD members",
          "Sub-Saharan Africa (excluding high income)","Sub-Saharan Africa","Sub-Saharan Africa (IDA & IBRD countries)","Turkiye"]
          data=data[~data["Country Name"].isin(ce)]
          column=data["Country Name"].drop_duplicates().tolist()
          user=Register_model.objects.get(Email=request.session['em'])    
          return render(request,'EduPrediction6.html',{"data":column,"user":user})




# Load saved models and scalers using memory mapping
label_encoder = joblib.load('label_encoder.pkl')
poly = joblib.load('poly_features.pkl')
scaler = joblib.load('scaler.pkl')
stacking_classifier = joblib.load('stacking_classifier.pkl')


def Student_Prediction(request):
    if request.method == 'POST':
        # Collect data directly from POST request
        marital_status = int(request.POST.get('Marital_status'))
        application_order = int(request.POST.get('Application_order'))
        application_mode = int(request.POST.get('Application_mode'))
        course = int(request.POST.get('Course'))
        Nationality = int(request.POST.get('Nationality'))
        daytime_evening_attendance = int(request.POST.get('Daytime_evening_attendance'))

        # Encode previous qualification
        previous_qualification = int(request.POST.get('Previous_qualification'))
        mothers_qualification = int(request.POST.get('Mothers_qualification'))
        fathers_qualification = int(request.POST.get('Fathers_qualification'))
        mothers_occupation = int(request.POST.get('Mothers_occupation'))
        fathers_occupation = int(request.POST.get('Fathers_occupation'))
        displaced = int(request.POST.get('Displaced'))
        Educational_Needs = int(request.POST.get('special_needs'))
        Debtors = int(request.POST.get('debtor'))
        Tution_fees = int(request.POST.get('tuition_fees'))
        Gender = int(request.POST.get('gender'))
        Scholarship = int(request.POST.get('scholarship_holder'))
        International = int(request.POST.get('international'))
        Unemployment = float(request.POST.get('unemployment_rate'))
        Age_Enroll = int(request.POST.get('age_enrollment'))
        Inflation = float(request.POST.get('inflation_rate'))
        GDP = float(request.POST.get('gdp'))

        # Curricular units
        units_1st_sem_enrolled = int(request.POST.get('curricular_units_1st_enrolled'))
        units_1st_sem_approved = int(request.POST.get('curricular_units_1st_approved'))
        grade_1st_sem = float(request.POST.get('curricular_units_1st_grade'))  # Fixed typo
        units_1st_sem_no_eval = int(request.POST.get('curricular_units_1st_without_evaluations'))

        units_2nd_sem_enrolled = int(request.POST.get('curricular_units_2nd_enrolled'))
        units_2nd_sem_approved = int(request.POST.get('curricular_units_2nd_approved'))
        grade_2nd_sem = float(request.POST.get('curricular_units_2nd_grade'))
        units_2nd_sem_no_eval = int(request.POST.get('curricular_units_2nd_without_evaluations'))

        errors = []

        # Validate relationships: approved units cannot be more than enrolled units
        if units_1st_sem_approved > units_1st_sem_enrolled:
            errors.append("1st Semester: Approved units cannot be greater than enrolled units.")
        if units_2nd_sem_approved > units_2nd_sem_enrolled:
            errors.append("2nd Semester: Approved units cannot be greater than enrolled units.")

        # Validate relationships: no evaluation units cannot exceed enrolled units
        if units_1st_sem_no_eval > units_1st_sem_enrolled:
            errors.append("1st Semester: Units without evaluations cannot be greater than enrolled units.")
        if units_2nd_sem_no_eval > units_2nd_sem_enrolled:
            errors.append("2nd Semester: Units without evaluations cannot be greater than enrolled units.")

        # Check if there are any errors
        if errors:
            # Return errors to the user
            return render(request, 'Student Prediction.html', {'errors': errors})

        # Prepare feature array for prediction
        features = np.array([[
            marital_status,
            application_order,
            application_mode,
            course,
            Nationality,
            daytime_evening_attendance,
            previous_qualification,
            mothers_qualification,
            fathers_qualification,
            mothers_occupation,
            fathers_occupation,
            displaced,
            Educational_Needs,
            Debtors,
            Tution_fees,
            Gender,
            Scholarship,
            International,
            Unemployment,
            Age_Enroll,
            Inflation,
            GDP,
            units_1st_sem_enrolled,
            units_1st_sem_approved,
            grade_1st_sem,
            units_1st_sem_no_eval,
            units_2nd_sem_enrolled,
            units_2nd_sem_approved,
            grade_2nd_sem,
            units_2nd_sem_no_eval
        ]])

        # Print the number of features for debugging
        print("Number of Features Collected:", features.shape[1])  # Should be 30

        # Check the number of features
        if features.shape[1] != 30:
            raise ValueError(f"Expected 30 features, but got: {features.shape[1]}")

        # Scaling and polynomial transformation
        features_poly = poly.transform(features)
        print("Transformed Features Shape:", features_poly.shape)  # Ensure it matches expected shape

        # Make the prediction using the loaded stacking classifier
        prediction = stacking_classifier.predict(features_poly)
        result = prediction[0]  # Get the prediction result
        result = label_encoder.inverse_transform([result])
        result = result[0]
        print(result)

        # Render the result page with the prediction result
        user = Register_model.objects.get(Email=request.session['em'])
        return render(request, 'Student Result.html', {'result': result,"user":user})

    # For GET requests, render the form
    user = Register_model.objects.get(Email=request.session['em'])
    return render(request, 'Student Prediction.html',{"user":user})

def Student_Analysis(request):
	user=Register_model.objects.get(Email=request.session['em'])
	return render(request,'Student Analysis.html',{'user':user})


def Student_EDA1(request):
    # Load the dataset
    data = pd.read_csv("dataset.csv")

    # Filter relevant columns for analysis
    df = data[['Unemployment rate', 'Inflation rate', 'GDP', 'Target']]

    # Group the data by 'Target' (Dropout or Graduate) and calculate the average of economic factors
    grouped_df = df.groupby('Target').mean().reset_index()

    # Create a bar chart to compare economic factors for Dropout vs. Graduate
    fig = px.bar(
        grouped_df,
        x='Target',
        y=['Unemployment rate', 'Inflation rate', 'GDP'],
        title='Average Economic Factors for Dropouts vs. Graduates',
        labels={'value': 'Average Value', 'Target': 'Student Outcome'},
        barmode='group',
        height=450
    )

    # Update layout for better visualization
    fig.update_layout(
        xaxis_title="Student Outcome",
        yaxis_title="Average Economic Factors",
        legend_title="Economic Factor",
        template="plotly"
    )

    # Convert the Plotly figure to HTML
    graph = fig.to_html()

    # Render the template with the graph
    return render(request, 'Student EDA1.html', {'graph': graph})

def Student_EDA2(request):
    # Load the dataset
    data = pd.read_csv("dataset.csv")

    # Count the occurrences of each 'Target' (Dropout or Graduate)
    target_count = data['Target'].value_counts().reset_index()

    # Rename columns for clarity
    target_count.columns = ['Target', 'Count']

    # Create a pie chart to show the distribution of Dropouts vs. Graduates vs. Enrolled
    fig = px.pie(
        target_count,
        names='Target',
        values='Count',
        title='Distribution of Student Outcomes: Dropouts vs. Graduates vs. Enrolled',
        hole=0.4  # Makes it a donut chart, if desired
    )

    # Update layout for better visualization
    fig.update_traces(textinfo='percent+label', pull=[0.1, 0])  # Emphasize one segment
    fig.update_layout(template="plotly")

    # Convert the Plotly figure to HTML
    graph = fig.to_html()

    # Render the template with the graph
    return render(request, 'Student EDA2.html', {'graph': graph})

def Student_EDA3(request):
    # Load the dataset
    data = pd.read_csv("dataset.csv")

    # Create DataFrame
    df = pd.DataFrame(data)

    # Map the columns for better readability
    df['Previous qualification'] = df['Previous qualification'].map({
        1: 'High School',
        2: 'Undergraduate',
        3: 'Postgraduate'
    })
    df['Daytime/evening attendance'] = df['Daytime/evening attendance'].map({
        1: 'Daytime',
        2: 'Evening'
    })

    # Filter the DataFrame for only Daytime attendance
    df_daytime = df[df['Daytime/evening attendance'] == 'Daytime']

    # Create a grouped bar plot to visualize the impact of Previous Qualification on graduation outcomes
    fig = px.histogram(
        df_daytime,  # Use the filtered DataFrame
        x='Previous qualification',  # The x-axis now represents Previous Qualification
        color='Target',  # Bars are colored based on the Target (Dropout, Graduate, Enrolled)
        barmode='group',  # Group bars together
        title="Impact of Previous Qualification on Graduation Outcomes (Daytime Only)",
        labels={'Previous qualification': 'Previous Qualification', 'Target': 'Outcome'},
        color_discrete_sequence=px.colors.qualitative.Set1  # Change color palette
    )

    # Customize the layout
    fig.update_layout(
        yaxis_title='Count of Outcomes',  # Update y-axis title
    )

    # Convert the Plotly figure to HTML
    graph = fig.to_html()

    # Render the template with the graph
    return render(request, 'Student EDA3.html', {'graph': graph})


def Student_EDA4(request):
    # Load the data from your path
    file_path = "dataset.csv"  # Replace with the actual path to your dataset
    df = pd.read_csv(file_path)

    # Aggregate data by 'Target' (Graduate or Dropout) to calculate totals
    agg_df = df.groupby('Target').agg({
        'Curricular units 2nd sem (approved)': 'sum',           # Sum of approved units
        'Curricular units 2nd sem (enrolled)': 'sum',           # Sum of enrolled units
        'Curricular units 2nd sem (without evaluations)': 'sum' # Sum of units without evaluations
    }).reset_index()

    # Reshape the data to have a long format for grouping
    agg_df_long = agg_df.melt(
        id_vars='Target',
        value_vars=[
            'Curricular units 2nd sem (approved)', 
            'Curricular units 2nd sem (enrolled)', 
            'Curricular units 2nd sem (without evaluations)'
        ],
        var_name='Metric', 
        value_name='Value'
    )

    # Create a grouped bar chart
    fig = px.bar(
        agg_df_long,
        x='Target',
        y='Value',
        color='Metric',
        barmode='group',  # Set bar mode to 'group'
        labels={
            'Value': 'Total Units',
            'Target': 'Outcome'
        },
        title="Grouped Bar Chart: Approved, Enrolled, and Units Without Evaluations by Outcome"
    )

    # Convert the Plotly figure to HTML
    graph = fig.to_html()

    # Render the template with the graph
    return render(request, 'Student EDA4.html', {'graph': graph})

def Student_EDA5(request):
    # Load the dataset
    data = pd.read_csv("dataset.csv")

    # Ensure 'Application mode' is treated as a string (for proper labeling)
    data['Application mode'] = data['Application mode'].astype(str)

    # Create a dictionary to map application mode values to the provided descriptive names
    application_mode_mapping = {
        '1': '1st Phase - General Contingent',
        '2': 'Ordinance No. 612/93',
        '3': '1st Phase - Special Contingent (Azores Island)',
        '4': 'Holders of Other Higher Courses',
        '5': 'Ordinance No. 854-B/99',
        '6': 'International Student (Bachelor)',
        '7': '1st Phase - Special Contingent (Madeira Island)',
        '8': '2nd Phase - General Contingent',
        '9': '3rd Phase - General Contingent',
        '10': 'Ordinance No. 533-A/99, Item b2) (Different Plan)',
        '11': 'Ordinance No. 533-A/99, Item b3 (Other Institution)',
        '12': 'Over 23 Years Old',
        '13': 'Transfer',
        '14': 'Change of Course',
        '15': 'Technological Specialization Diploma Holders',
        '16': 'Change of Institution/Course',
        '17': 'Short Cycle Diploma Holders',
        '18': 'Change of Institution/Course (International)'
    }

    # Use the apply method to replace 'Application mode' values with descriptive names
    data['Application mode'] = data['Application mode'].apply(lambda x: application_mode_mapping.get(x))

    # Group by 'Application mode' and count the number of students enrolled in the second semester
    enrollment_counts = data.groupby('Application mode')['Curricular units 2nd sem (enrolled)'].sum().reset_index()

    # Create a bar chart to show the enrollment count in the second semester for each application mode
    fig = px.bar(
        enrollment_counts,
        x='Application mode',
        y='Curricular units 2nd sem (enrolled)',
        title='2nd Semester Enrollment by Application Mode',
        labels={'Curricular units 2nd sem (enrolled)': 'Enrollment Count', 'Application mode': 'Application Mode'},
        color='Application mode',
        height=600
    )

    # Update layout for better visualization
    fig.update_layout(template="plotly")

    # Convert the Plotly figure to HTML
    graph = fig.to_html()

    # Render the template with the graph
    return render(request, 'Student EDA5.html', {'graph': graph})


def Student_EDA6(request):
    # Load the dataset
    data = pd.read_csv("dataset.csv")

    # If 'Gender' is represented as 0, 1, etc., map them to actual names
    gender_map = {0: 'Male', 1: 'Female'}  # Adjust the mapping as needed based on your dataset
    data['Gender'] = data['Gender'].map(gender_map)

    # Count occurrences of each 'Target' (Dropout, Graduate, Enrolled) by 'Gender'
    target_gender_count = data.groupby(['Gender', 'Target']).size().reset_index(name='Count')

    # Create a grouped bar chart to show the distribution of outcomes by gender
    fig = px.bar(
        target_gender_count,
        x='Gender',
        y='Count',
        color='Target',
        barmode='group',  # This creates the grouped bar chart
        title='Distribution of Student Outcomes by Gender',
        category_orders={'Gender': ['Male', 'Female', 'Other']}  # Specify the gender categories explicitly
    )

    # Update layout for better visualization
    fig.update_layout(template="plotly", yaxis_title='Count', xaxis_title='Gender')

    # Convert the Plotly figure to HTML
    graph = fig.to_html()

    # Render the template with the graph
    return render(request, 'Student EDA6.html', {'graph': graph})


def Student_EDA7(request):
    # Load the dataset
    data = pd.read_csv("dataset.csv")

    # Group by 'Target' and calculate the average grade for the first semester
    avg_grades = data.groupby('Target')['Curricular units 1st sem (grade)'].mean().reset_index()

    # Create a donut chart to show the average grade in the first semester for each student outcome
    fig = px.pie(
        avg_grades,
        values='Curricular units 1st sem (grade)',
        names='Target',
        title='Average 1st Semester Grade for Each Student Outcome',
        hole=0.4,  # Makes it a donut chart
        labels={'Curricular units 1st sem (grade)': 'Average Grade', 'Target': 'Student Outcome'},
        color='Target'
    )

    # Update layout for better visualization
    fig.update_traces(textinfo='percent+label')  # Show percentage and label
    fig.update_layout(template="plotly")

    # Convert the Plotly figure to HTML
    graph = fig.to_html()

    # Render the template with the graph
    return render(request, 'Student EDA7.html', {'graph': graph})


def Chatbot(request):
	user=Register_model.objects.get(Email=request.session['em'])
	return render(request,'Chatbot.html',{'user':user})