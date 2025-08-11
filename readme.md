# Autobooking sessions on octiv
This script should allow you to book automatically sessions on octiv using your JWT token which is valid for 1 year.
Meaning that you will have to change the token each year.
# Requirements
1. You will need a Linux server or a machine that is always on with python > 3.10
2. Have access to the crontab -e on the machine.
3. Access to an octiv account.
4. JWT token which you should be able to get from your browser.

# Steps
1. ssh to your server
1. Set the secret as an environment variable. in order to get these information you will have to inspect the requests on the browser. Below is a json an example of a `class-bookings` payload that you can check for reference
<details>
<summary>Show JSON</summary>
```json
{
    "id": 32266371,
    "statusId": 1,
    "status": {
        "id": 1,
        "name": "BOOKED"
    },
    "isTopUpUsed": null,
    "checkedInAt": null,
    "checkedOutAt": null,
    "classId": 211972,
    "class": {
        "id": 211972,
        "name": "CrossFit 06:30", // I use this to filter the class_name of the course. that's why i use 6:30
        "description": "",
        "image": null,
        "type": {
            "id": 2,
            "name": "RECURRING"
        },
        "startTime": "2025-08-11 06:30:00",
        "endTime": "2025-08-11 07:30:00",
        "recurringStartDate": "2024-07-30",
        "recurringEndDate": null,
        "recurringInterval": 1,
        "isVirtual": 0,
        "isSession": 0,
        "isFree": 0,
        "isActive": 1,
        "isVisibleInApp": 1,
        "isDisplayInstructorName": 1,
        "limit": 8,
        "bookingThreshold": 1,
        "cancellationThreshold": 1,
        "minBookedMembersCount": 1,
        "autoCancelThresholdMin": 480,
        "meetingUrl": null,
        "tenantId": 102326,
        "locationId": 1981,
        "location": {
            "id": 1981,
            "name": "CrossFit RULER",
            "businessName": "CrossFit RULER",
            "vat": null,
            "invoiceInformation": null,
            "logoUrl": null,
            "description": null,
            "phoneNumber": null,
            "attendanceCode": null,
            "imageOne": null,
            "imageTwo": null,
            "imageThree": null,
            "imageFour": null,
            "coverImageUrl": null,
            "prefix": "CFRL",
            "deactivatedAt": null,
            "canDebit": 1,
            "isActive": 1,
            "additionalFeatures": [],
            "hasRequestCancellation": 0,
            "tenantId": 102326,
            "tenant": {
                "id": 102326,
                "statusId": 1,
                "status": {
                    "id": 1,
                    "name": "ACTIVE"
                },
                "name": "CrossFit RULER",
                "description": null,
                "websiteUrl": null,
                "instagramUrl": null,
                "facebookUrl": null,
                "createdAt": "2024-05-17 15:01:41",
                "updatedAt": "2025-08-05 12:30:37",
                "isTrial": 0,
                "isSignUpUseContracts": 1,
                "isSignUpUseWaivers": 1,
                "signUpRequiredFields": [],
                "workoutThreshold": 0,
                "signUpPaymentOptions": [
                    1,
                    2,
                    5,
                    "1"
                ],
                "signUpDebitDayOptions": [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7
                ],
                "limitInterFacilityBookings": 0,
                "subscriptionCollectionDays": null,
                "deactivatedAt": null,
                "regionId": 60,
                "tenantBillingCurrencyId": 47,
                "memberBillingCurrencyId": 47,
                "timezoneId": 181,
                "timezone": {
                    "id": 181,
                    "name": "W. Europe Standard Time",
                    "description": "(UTC+01:00) Amsterdam, Berlin, Bern, Rome, Stockholm, Vienna",
                    "abbr": "WEDT",
                    "zone": "Europe/Luxembourg",
                    "offset": "2",
                    "isDaylightSaving": 1
                }
            },
            "billingPaymentGatewayId": 9,
            "paymentGatewayId": 8,
            "timezoneId": null,
            "timezone": null,
            "categoryId": 1,
            "createdAt": "2024-05-17 15:02:22",
            "updatedAt": "2025-08-10 18:39:48",
            "addressId": null,
            "address": null,
            "settings": {
                "allowImagesForClasses": 0,
                "allowImagesForSessions": 0
            },
            "billingGatewayOnboarded": true,
            "gracePeriodStart": null,
            "gracePeriodEnd": null,
            "gracePeriodDays": 0,
            "financePaymentToken": null
        },
        "instructorId": 451268,
        "instructor": {
            "id": 451268,
            "name": "xxxx",
            "surname": "xxxx",
            "email": "xxxx",
            "dateOfBirth": "xxxxxxxx",
            "age": 41,
            "idNumber": null,
            "address": null,
            "addressId": null,
            "mobile": "+xxxxx",
            "typeId": 11,
            "type": {
                "id": 11,
                "name": "USER"
            },
            "gender": null,
            "image": "https://octiv-prod-public-newy2432.eu-central-1.linodeobjects.com/profile-images/1309193169664ddecba31251.01281117.png",
            "medicalCondition": null,
            "emergencyContactName": "xxxxxxxxx",
            "emergencyContactMobile": "+xxxxxxxxx",
            "healthProviderId": null,
            "hasAcceptedTermsAndConditions": true,
            "paymentMethod": null,
            "createdAt": "2024-05-17 15:01:42",
            "updatedAt": "2024-06-10 04:15:36",
            "deleted": 0,
            "isRedacted": 0
        },
        "supportingInstructorId": null,
        "supportingInstructor": null,
        "settings": {
            "colours": {
                "border": null
            }
        }
    },
    "classDateId": 19850115,
    "leadMemberId": null,
    "userId": xxxx, // this is your userId
    "userPackageId": xxxxxx,
    "createdById": xxxx,
    "updatedById": null,
    "createdAt": "2025-08-11 12:33:10",
    "updatedAt": "2025-08-11 12:33:10"
}
```
</details>

```sh
export OCTIV_TOKEN="TOKEN_HERE" # this is the bearer token which you shall find in any http request sent to the backend. 
export USER_ID="YOUR_USERID_HERE" # You should able to get by simulating a `class-bookings` request and you will find all the details in the payload
export CLASS_NAME="6:30" # I am always at 6:30 so the value should be 6:30
```
<details>
<summary>Show JSON</summary>
```json
{
    "id": 32266371,
    "statusId": 1,
    "status": {
        "id": 1,
        "name": "BOOKED"
    },
    "isTopUpUsed": null,
    "checkedInAt": null,
    "checkedOutAt": null,
    "classId": 211972,
    "class": {
        "id": 211972,
        "name": "CrossFit 06:30", // I use this to filter the class_name of the course. that's why i use 6:30
        "description": "",
        "image": null,
        "type": {
            "id": 2,
            "name": "RECURRING"
        },
        "startTime": "2025-08-11 06:30:00",
        "endTime": "2025-08-11 07:30:00",
        "recurringStartDate": "2024-07-30",
        "recurringEndDate": null,
        "recurringInterval": 1,
        "isVirtual": 0,
        "isSession": 0,
        "isFree": 0,
        "isActive": 1,
        "isVisibleInApp": 1,
        "isDisplayInstructorName": 1,
        "limit": 8,
        "bookingThreshold": 1,
        "cancellationThreshold": 1,
        "minBookedMembersCount": 1,
        "autoCancelThresholdMin": 480,
        "meetingUrl": null,
        "tenantId": 102326,
        "locationId": 1981,
        "location": {
            "id": 1981,
            "name": "CrossFit RULER",
            "businessName": "CrossFit RULER",
            "vat": null,
            "invoiceInformation": null,
            "logoUrl": null,
            "description": null,
            "phoneNumber": null,
            "attendanceCode": null,
            "imageOne": null,
            "imageTwo": null,
            "imageThree": null,
            "imageFour": null,
            "coverImageUrl": null,
            "prefix": "CFRL",
            "deactivatedAt": null,
            "canDebit": 1,
            "isActive": 1,
            "additionalFeatures": [],
            "hasRequestCancellation": 0,
            "tenantId": 102326,
            "tenant": {
                "id": 102326,
                "statusId": 1,
                "status": {
                    "id": 1,
                    "name": "ACTIVE"
                },
                "name": "CrossFit RULER",
                "description": null,
                "websiteUrl": null,
                "instagramUrl": null,
                "facebookUrl": null,
                "createdAt": "2024-05-17 15:01:41",
                "updatedAt": "2025-08-05 12:30:37",
                "isTrial": 0,
                "isSignUpUseContracts": 1,
                "isSignUpUseWaivers": 1,
                "signUpRequiredFields": [],
                "workoutThreshold": 0,
                "signUpPaymentOptions": [
                    1,
                    2,
                    5,
                    "1"
                ],
                "signUpDebitDayOptions": [
                    1,
                    2,
                    3,
                    4,
                    5,
                    6,
                    7
                ],
                "limitInterFacilityBookings": 0,
                "subscriptionCollectionDays": null,
                "deactivatedAt": null,
                "regionId": 60,
                "tenantBillingCurrencyId": 47,
                "memberBillingCurrencyId": 47,
                "timezoneId": 181,
                "timezone": {
                    "id": 181,
                    "name": "W. Europe Standard Time",
                    "description": "(UTC+01:00) Amsterdam, Berlin, Bern, Rome, Stockholm, Vienna",
                    "abbr": "WEDT",
                    "zone": "Europe/Luxembourg",
                    "offset": "2",
                    "isDaylightSaving": 1
                }
            },
            "billingPaymentGatewayId": 9,
            "paymentGatewayId": 8,
            "timezoneId": null,
            "timezone": null,
            "categoryId": 1,
            "createdAt": "2024-05-17 15:02:22",
            "updatedAt": "2025-08-10 18:39:48",
            "addressId": null,
            "address": null,
            "settings": {
                "allowImagesForClasses": 0,
                "allowImagesForSessions": 0
            },
            "billingGatewayOnboarded": true,
            "gracePeriodStart": null,
            "gracePeriodEnd": null,
            "gracePeriodDays": 0,
            "financePaymentToken": null
        },
        "instructorId": 451268,
        "instructor": {
            "id": 451268,
            "name": "xxxx",
            "surname": "xxxx",
            "email": "xxxx",
            "dateOfBirth": "xxxxxxxx",
            "age": 41,
            "idNumber": null,
            "address": null,
            "addressId": null,
            "mobile": "+xxxxx",
            "typeId": 11,
            "type": {
                "id": 11,
                "name": "USER"
            },
            "gender": null,
            "image": "https://octiv-prod-public-newy2432.eu-central-1.linodeobjects.com/profile-images/1309193169664ddecba31251.01281117.png",
            "medicalCondition": null,
            "emergencyContactName": "xxxxxxxxx",
            "emergencyContactMobile": "+xxxxxxxxx",
            "healthProviderId": null,
            "hasAcceptedTermsAndConditions": true,
            "paymentMethod": null,
            "createdAt": "2024-05-17 15:01:42",
            "updatedAt": "2024-06-10 04:15:36",
            "deleted": 0,
            "isRedacted": 0
        },
        "supportingInstructorId": null,
        "supportingInstructor": null,
        "settings": {
            "colours": {
                "border": null
            }
        }
    },
    "classDateId": 19850115,
    "leadMemberId": null,
    "userId": xxxx, // this is your userId
    "userPackageId": xxxxxx,
    "createdById": xxxx,
    "updatedById": null,
    "createdAt": "2025-08-11 12:33:10",
    "updatedAt": "2025-08-11 12:33:10"
}
```
</details>

1. Save the `octiv.py` file in your homedir (mine is root, i know...)
1. Once you have everything ready, it's time to set your `cronjob` by running `crontab -e` and edit the file by adding the following lines:

```sh
31 4 * * 0,1,2,3,4,5,6 /usr/bin/python3 /root/octiv.py >> octiv.logs # for GMT+2
31 5 * * 0,1,2,3,4,5,6 /usr/bin/python3 /root/octiv.py >> octiv.logs # for GMT+1
19 7 * * 0,1,2,3,4,5,6 /usr/bin/python3 /root/octiv.py >> octiv.logs # for some other reason
```