import { Component, OnInit, ViewChild, ɵConsole, NgZone } from '@angular/core';
import { FormGroup, FormBuilder, Validators } from "@angular/forms";
import { Router, ActivatedRoute } from '@angular/router';
import { HttpClient } from '@angular/common/http';
import { Title } from '@angular/platform-browser';

import { Observable } from 'rxjs';
import { switchMap } from 'rxjs/operators';
import { GoogleAnalyticsService } from 'ngx-google-analytics';
import { StripeService, StripeCardComponent } from 'ngx-stripe';
import { StripeCardElementOptions, StripeElementsOptions, PaymentIntent } from '@stripe/stripe-js';

import { PaymentService } from '../services/payment.service';
import { ToastService } from '../services/toast.service';

@Component({
	selector: 'app-checkout',
	templateUrl: './checkout.component.html',
	styleUrls: ['./checkout.component.scss']
})
export class CheckoutComponent implements OnInit {
	@ViewChild(StripeCardComponent) card: StripeCardComponent;
	successfulPaymentRedirectUrl: string = '/create-board';
	finishedLoading: boolean = false;
	paymentIntent: PaymentIntent | any;
	paymentProcessing: boolean = false;
	promoCode: string = '';
	loadingNewPrice: boolean = false;

	cardOptions: StripeCardElementOptions = {
		style: {
			base: {
				color: "#32325d",
				fontSmoothing: "antialiased",
				fontSize: "20px",
				"::placeholder": {
					color: "#32325d"
				}
			},
			invalid: {
				fontFamily: 'Arial, sans-serif',
				color: "#fa755a",
				iconColor: "#fa755a"
			}
		}
	}

	elementsOptions: StripeElementsOptions = {};

	formGroup: FormGroup;

	constructor(private fb: FormBuilder,
	            private titleService: Title,
				private stripeService: StripeService,
				private paymentService: PaymentService,
				private toastService: ToastService,
				private gaService: GoogleAnalyticsService,
				private router: Router,
				private ngZone: NgZone) {}

	ngOnInit(): void {
		this.titleService.setTitle('Checkout | SmorgasBoard');

		this.paymentService.createPaymentIntent()
		.then(paymentIntent => {
			this.paymentIntent = paymentIntent;
		})
		.catch(err => {
			console.error(err);
		})
		.finally(() => {
			this.finishedLoading = true;
		});
	}

	submitCouponCode(): void {
		let promoCode = this.promoCode;
		this.promoCode = '';
		this.loadingNewPrice = true;
		this.paymentService.createPaymentIntent(promoCode)
		.then(paymentIntent => {
			this.toastService.show(`Promo code ${promoCode} applied successfully!`);
			this.paymentIntent = paymentIntent;
			if (this.paymentIntent.amount == 0) {
				this.ngZone.run(() => {
					this.router.navigate([this.successfulPaymentRedirectUrl]);
				});
			}
		})
		.catch(err => {
			console.error(err.response.data);
			this.toastService.error(`Promo code ${promoCode} could not be applied. Reason: ${err.response.data.error}`);
		})
		.finally(() => {
			this.loadingNewPrice = false;
		});
	}

	pay(): void {
		this.paymentProcessing = true;
		this.stripeService.confirmCardPayment(
			this.paymentIntent.client_secret,
			{
				payment_method: {
					card: this.card.element
				}
			}
		)
		.subscribe((result) => {
			if (result.error) {
				// Show error to your customer (e.g., insufficient funds)
				console.log('Error: ' + result.error.message);
				this.toastService.error(`Error processing payment: ${result.error.message}`);
				this.paymentProcessing = false;
			} else {
				console.log("Payment successful");
				this.gaService.event('payment');
				// The payment has been processed!
				if (result.paymentIntent.status === 'succeeded') {
					this.toastService.show('Payment processed successfully. Thank you!');
				};
				this.paymentProcessing = false;

				this.ngZone.run(() => {
					this.router.navigate([this.successfulPaymentRedirectUrl]);
				});
			}
		});
	}
}
