from fastapi import APIRouter, Depends, Query, HTTPException, status
from app.services.calculator_service import CalculatorServices
from app.services.depreciation_calculator import PenyusutanCalculatorServices

router = APIRouter(prefix="/calculator", tags=["Calculator"])

@router.get("/addition", status_code=status.HTTP_200_OK)
def addition(
    num1: float = Query(..., description="First number"), 
    num2: float = Query(..., description="Second number"), 
    service: CalculatorServices = Depends()
):
    result = service.addition(num1, num2)
    return {"operation": "addition", "num1": num1, "num2": num2, "result": result}

@router.get("/subtraction", status_code=status.HTTP_200_OK)
def subtraction(
    num1: float = Query(..., description="First number"), 
    num2: float = Query(..., description="Second number"), 
    service: CalculatorServices = Depends()
):
    result = service.subtraction(num1, num2)
    return {"operation": "subtraction", "num1": num1, "num2": num2, "result": result}

@router.get("/multiplication", status_code=status.HTTP_200_OK)
def multiplication(
    num1: float = Query(..., description="First number"), 
    num2: float = Query(..., description="Second number"), 
    service: CalculatorServices = Depends()
):
    result = service.multiplication(num1, num2)
    return {"operation": "multiplication", "num1": num1, "num2": num2, "result": result}

@router.get("/division", status_code=status.HTTP_200_OK)
def division(
    num1: float = Query(..., description="First number"), 
    num2: float = Query(..., description="Second number"), 
    service: CalculatorServices = Depends()
):
    try:
        result = service.division(num1, num2)
        return {"operation": "division", "num1": num1, "num2": num2, "result": result}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router.get("/penyusutan", status_code=status.HTTP_200_OK)
def penyusutan(
    harga_perolehan: float = Query(..., description="Acquisition cost (must be > 0)"),
    estimasi_umur: float = Query(..., description="Estimated useful life in years (must be > 0)"),
    estimasi_nilai_sisa: float = Query(0, description="Residual value at the end of useful life (>= 0)"),
    metode: str = Query(..., description="Depreciation method ('straight_line' or 'double_declining')"),
    service: PenyusutanCalculatorServices = Depends()
):
    try:
        if metode not in ["straight_line", "double_declining"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Invalid method. Choose 'straight_line' or 'double_declining'."
            )
        
        if metode == "straight_line":
            biaya_per_bulan, biaya_per_tahun = service.straight_line(
                harga_perolehan, estimasi_umur, estimasi_nilai_sisa
            )
            return {
                "metode": metode,
                "biaya_per_bulan": biaya_per_bulan,
                "biaya_per_tahun": biaya_per_tahun,
            }
        else:
            biaya_per_bulan_list, biaya_per_tahun_list = service.double_declining(
                harga_perolehan, estimasi_umur, estimasi_nilai_sisa
            )
            return {
                "metode": metode,
                "biaya_per_bulan": biaya_per_bulan_list,
                "biaya_per_tahun": biaya_per_tahun_list,
            }
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
