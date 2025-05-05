from celery import shared_task
from .models import PortfolioRequest, PortfolioResult, PortfolioResultItem, SecuritiesMarket
from account.models import MemberBalance


LIMIT_RATIO = 0.3
@shared_task
def run_portfolio_progress(request_no):
    try:
        request_obj = PortfolioRequest.objects.get(no=request_no)
        request_obj.status = 1
        request_obj.message = ''
        request_obj.save(update_fields=["status", "message"])

        balance_ratio = request_obj.balance_ratio
        if not balance_ratio:
            request_obj.status = 4
            request_obj.message = "잔고 사용 비율이 올바르지 않습니다."
            request_obj.save(update_fields=["status", "message"])
            return

        balance_obj = MemberBalance.objects.filter(member_no=request_obj.member_no).first()
        if not balance_obj:
            request_obj.status = 4
            request_obj.message = "사용자 잔고 정보가 존재하지 않습니다."
            request_obj.save(update_fields=["status", "message"])
            return

        total_amount = int(balance_obj.amount * balance_ratio)
        limit_per_security = int(total_amount * LIMIT_RATIO)
        remaining = total_amount
        portfolio = {}

 
        while True:
            try:
                security = SecuritiesMarket.objects.filter(
                        price__gt=0, price__lte=remaining
                    ).order_by('?').first()
            except StopIteration:
                break

            if not security: break

            if security.price > remaining: continue

            max_per_security = min(remaining, limit_per_security)
            units = max_per_security // security.price

            amount = units * security.price
            remaining -= amount

            if security.code in portfolio:
                portfolio[security.code]["units"] += units
                portfolio[security.code]["amount"] += amount
            else:
                portfolio[security.code] = {
                    "security": security,
                    "units": units,
                    "amount": amount
                }

        if not portfolio:
            request_obj.status = 4
            request_obj.message = "투자 가능한 증권이 없습니다."
            request_obj.save(update_fields=["status", "message"])
            return

        result = PortfolioResult.objects.create(
            request_no=request_obj.no,
            invested_balance=total_amount - remaining
        )

        for p in portfolio.values():
            PortfolioResultItem.objects.create(
                result_no=result.no,
                security_code=p["security"].code,
                security_name=p["security"].name,
                price=p["security"].price,
                units=p["units"],
                amount=p["amount"]
            )

        request_obj.status = 2
        request_obj.message = ''
        request_obj.save(update_fields=["status", "message"])

    except PortfolioRequest.DoesNotExist:
        print(f"자문 요청 {request_no} 없음")
    except Exception as e:
        print(f"자문 실패: {e}")
        try:
            request_obj.status = 4
            request_obj.message = f"서버 에러로 인한 자문 실패"
            request_obj.save(update_fields=["status", "message"])
        except:
            pass
