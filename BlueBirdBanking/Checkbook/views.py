from django.shortcuts import render, redirect, get_object_or_404
from .forms import AccountForm, TransactionForm
from .models import Account, Transaction

# Create your views here.
# renders home page when requested
def home(request):
    form = TransactionForm(data=request.POST or None) #gets transaction form
    if request.method == 'POST':
        pk = request.POST['account'] # if form is submitted, retrieve account user wants to view
        return balance(request, pk) # call balance function to render BalanceSheet.html
    content = { 'form': form }
    return render(request, 'checkbook/index.html', content)

# renders create new account page when requested
def create_account(request):
    form = AccountForm(data=request.POST or None) # retrieve the account form
    # checks if method is POST
    if request.method == 'POST':
        if form.is_valid(): # checks if form is valid
            form.save() # saves form if valid
            return redirect('index') # sends user back to homepage
    content = { 'form': form } # saves form data to template as a dictionary
    # adds content of form to page
    return render(request, 'checkbook/CreateNewAccount.html', content)

# renders Balance page when requested
def balance(request, pk):
    account = get_object_or_404(Account, pk=pk)
    transactions = Transaction.Transactions.filter(account=pk) # retrieve all account transactions matching pk
    current_total = account.initial_deposit # create account total variable starting with initial deposit
    table_contents = {} # create dictionary to store transaction information
    for t in transactions:
        if t.type == 'Deposit':
            current_total += t.amount # add deposits to balance
            table_contents.update({t: current_total}) # add transaction and total to dictionary
        else:
            current_total -= t.amount # subtracts withdrawals from balance
            table_contents.update({t: current_total})
    content = { 'account': account, 'table_contents': table_contents, 'balance': current_total }
    return render(request, 'checkbook/BalanceSheet.html', content)

# renders Transaction page when requested
def transaction(request):
    form = TransactionForm(data=request.POST or None) # gets transaction form
    if request.method == 'POST':
        pk = request.POST['account']
        form.save()
        return balance(request, pk)
    content = { 'form': form }
    return render(request, 'checkbook/AddTransaction.html', content)

