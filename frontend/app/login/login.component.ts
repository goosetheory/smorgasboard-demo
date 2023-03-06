import { Component, OnInit, ChangeDetectorRef, NgZone } from '@angular/core';
import { onAuthUIStateChange, CognitoUserInterface, AuthState, FormFieldTypes } from '@aws-amplify/ui-components';
import { Title } from '@angular/platform-browser';
import { Router, ActivatedRoute } from '@angular/router';
import config from '../../aws-exports';
import{ Amplify, Auth } from 'aws-amplify';

@Component({
	selector: 'app-login',
	templateUrl: './login.component.html',
	styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
	private previousAuthState: AuthState = null;
	private signinRedirectUrl: string;
	private signinRedirectParams: object;
	private defaultRedirectUrl: string = "/get-started";

	signupFormFields: FormFieldTypes;
	user: CognitoUserInterface | undefined;
	authState: AuthState;

	constructor(private titleService: Title,
	            private ref: ChangeDetectorRef,
				private route: ActivatedRoute,
				private router: Router,
				private ngZone: NgZone) {
		this.signinRedirectUrl = this.router.getCurrentNavigation().extras.state?.redirectUrl || null;
		this.signinRedirectParams = this.router.getCurrentNavigation().extras.state?.redirectParams || null;

		this.signupFormFields = [
		{
			type: "given_name",
			label: "Given Name",
			placeholder: "required",
			required: true,
		},
		{
			type: "email",
			label: "Email",
			placeholder: "required",
			required: true,
		},
		{
			type: "password",
			label: "Password",
			placeholder: "required",
			required: true,
		}];
	}

	ngOnInit() {
		this.titleService.setTitle('Sign Up / Log In | SmorgasBoard');

		onAuthUIStateChange((authState, authData) => {
			this.authState = authState;
			this.user = authData as CognitoUserInterface;
			this.ref.detectChanges();

			// Don't want to nav if we're signed in and click "log out. Thus, previous auth state.
			if (this.authState == AuthState.SignedIn && this.previousAuthState && this.previousAuthState != AuthState.SignedIn) {
				this.previousAuthState = null; // Reset auth state, since we're navving away
				if (this.signinRedirectUrl) {
					this.ngZone.run(() => {
						this.router.navigate([this.signinRedirectUrl], { queryParams: this.signinRedirectParams });
					});
				} else {
					this.ngZone.run(() => {
						this.router.navigate([this.defaultRedirectUrl]);
					});
				}
			}

			this.previousAuthState = authState;
		})
	}

	isSignedIn(): boolean {
		return this.authState == AuthState.SignedIn;
	}

	ngOnDestroy() {
		return onAuthUIStateChange;
	}

	private getQueryParams(url: string): any {

	}
}
