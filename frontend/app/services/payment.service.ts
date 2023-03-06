import { Injectable } from '@angular/core';
import { API } from 'aws-amplify';

import { BaseService } from './base-service';
import { PaymentIntent } from '@stripe/stripe-js';
import { Payment } from '../dtos/Payment';
import { PaymentStatus } from '../dtos/PaymentStatus';

@Injectable({
	providedIn: 'root'
})
export class PaymentService extends BaseService {
	private apiName = 'BoardAPI';
	private authenticatedPaymentPath = '/payments';
	private authenticatedPaymentIntentPath = '/payments/intents';

	async createPaymentIntent(couponCode = null): Promise<PaymentIntent | any> {
		const init = await super.getInit();
		if (couponCode) {
			init.body = {
				'couponCode': couponCode
			};
		}

		return API
		.post(this.apiName, this.authenticatedPaymentIntentPath, init);
	}

	async getSuccessfulPayments(): Promise<Payment[]> {
		const init = await super.getInit();
		let pathWithArgs = this.authenticatedPaymentPath + `?paymentStatus=${PaymentStatus.Succeeded}`

		return API
		.get(this.apiName, pathWithArgs, init)
		.then(results => {
			return results.map(Payment.fromWire);
		})
	}
}
