from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Election , VoteBlocks , Candidate
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from .forms import PasswordChangeForm  
from .forms import UserProfileForm  
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .blockchain import Blockchain
from django.db.models import Count



import datetime
import hashlib
import json

def register(request):
    if request.method == 'POST':
        # Handle registration logic here
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        email = request.POST['email']
        phone_number = request.POST['phone_number']

        # Perform validation and user creation here
        # Ensure password and confirm_password match
        if password == confirm_password:
            # Check if the username is already taken
            if User.objects.filter(username=username).exists():
                # Username is already taken, handle this error
                pass
            else:
                # Create user account
                user = User(username=username, email=email)
                user.set_password(password)
                user.save()

                # Create and save the user profile with all fields
                profile = UserProfile(user=user, phone_number=phone_number, name=username, email=email)
                profile.save()

                return redirect('login')  # Redirect to login page after successful registration
        else:
            # Passwords do not match, handle this error
            pass
    return render(request, 'register.html')



def user_login(request):
    if request.method == 'POST':
        # Handle login logic here
        username = request.POST['username']
        password = request.POST['password']

        # Check if the user exists
        user = User.objects.filter(username=username).first()
        if user is not None and user.check_password(password):
            login(request, user)
            return redirect('dashboard')  
        else:
            pass
    return render(request, 'login.html')




def user_logout(request):
    logout(request)
    return redirect('register')

@login_required
def edit_profile(request):
    user_profile = UserProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = UserProfileForm(instance=user_profile)
    
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully.')
            return redirect('change_password')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'change_password.html', {'form': form})

@login_required
def dashboard(request):
    user_profile = UserProfile.objects.get(user=request.user)
    elections = Election.objects.all()
    return render(request, 'dashboard.html', {'user_profile': user_profile, 'elections': elections})


@login_required
def view_election_details(request, election_id):
    election = get_object_or_404(Election, pk=election_id)
    candidates = Candidate.objects.filter(election=election)
    return render(request, 'election_details.html', {'election': election, 'candidates': candidates})






@login_required
def cast_vote(request, election_id, candidate_id):
    user = request.user
    candidate = get_object_or_404(Candidate, id=candidate_id)

    # Check if the election is completed
    election = get_object_or_404(Election, id=election_id)
    if election.status == 'completed':
        return HttpResponse("Voting for this election has ended. You can no longer vote.")
    elif election.status != 'ongoing':
        return HttpResponse("Voting for this election is not currently allowed. Please check the election status.")

    # Check if the user has already voted in this election
    if VoteBlocks.objects.filter(user=user, candidate__election=election).exists():
        return HttpResponse("You have already voted in this election.")

    # Create a new block for the blockchain
    blockchain = Blockchain()
    previous_block = blockchain.get_previous_block()
    previous_hash = blockchain.hash(previous_block)
    proof = blockchain.proof_of_work(previous_block['proof'])
    block_data = {
        'user_id': user.id,
        'candidate_id': candidate_id,
        'timestamp': str(datetime.datetime.now())
    }
    new_block = {
        'index': len(blockchain.chain) + 1,
        'timestamp': str(datetime.datetime.now()),
        'proof': proof,
        'previous_hash': previous_hash,
        'data': block_data,
    }
    blockchain.chain.append(new_block)

    # Create a VoteBlocks instance to store the vote details
    vote_block = VoteBlocks(
        user=user,
        candidate=candidate,
        Block_Hash=previous_hash,
    )
    vote_block.save()

    return HttpResponse("Your vote has been recorded with blockchain code: " + previous_hash)


def election_results(request):
    # Get all completed elections
    completed_elections = Election.objects.filter(status='completed')

    election_results = []

    for election in completed_elections:
        # Get the candidates for each completed election and count their votes
        candidates = Candidate.objects.filter(election=election)
        results = candidates.annotate(vote_count=Count('voteblocks'))

        # Sort the results by the number of votes in descending order
        results = results.order_by('-vote_count')

        # Check if there are multiple winners with the same number of votes
        top_votes = results[0].vote_count
        winners = [candidate for candidate in results if candidate.vote_count == top_votes]

        election_result = {
            'election': election,
            'winners': winners,
        }

        election_results.append(election_result)

    return render(request, 'election_results.html', {'election_results': election_results})
