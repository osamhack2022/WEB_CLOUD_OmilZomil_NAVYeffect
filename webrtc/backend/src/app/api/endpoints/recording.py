import base64
import numpy as np
import cv2
import sys

from typing import List
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import cv2
import numpy as np
import base64
from datetime import datetime
import traceback
from loguru import logger

import uuid

from app.api import deps
from app.api.manager.broker import SingleBroker
from app.api.websocket.image import photo_2_img, img_2_photo
from app.api.db.guardhouse import get_guardhouse, select_guardhouse
from app.ai.OZEngine.model import OmilZomil



router = APIRouter()

    
@router.websocket("/test")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(deps.get_db)):
    """
    ai 요구사항만 맞춰서 실행
    병렬 처리 X
    버퍼 X - 파일로 저장 X
    단지 카메라 객체만 유지
    """
    # id, time
    connect_start_time = datetime.now()
    camera_id = str(uuid.uuid4())

    # 처음 접속 =  위병소 리스트 전달
    await websocket.accept()
    house_list = [data.house for data in get_guardhouse(db)]
    await websocket.send_json({
        'type' : "list",
        'list' : house_list,
    })

    print("소캣 연결 완료")
    omil_detecter = OmilZomil()
    
    # 수신 중
    print(" 이미지 수신 시작")
    try:
        while True:
            data = await websocket.receive_json()
            work_start = datetime.now()

            img = photo_2_img(data['photo'])
            # 임시로 모든 이미지 저장
            cv2.imwrite(f"./image_list/{camera_id}_{work_start.strftime('%H-%M-%S')}.jpg", img)

            print(f'데이터 수신:- {camera_id}')
            report = omil_detecter.detect(img)
            print(report)
            print(report['step'])
            print(report.get('component'))

            msg = {
                'type' : "ai",
                'step' : report['step'],
                'component' : report.get('component'),
            }
            await websocket.send_json(msg)
            # 1차 처리 로그 출력
            print(f'테스크 1차 처리 완료: {camera_id} : {datetime.now() - work_start}')
            print()
            print()


    except WebSocketDisconnect:
        print(f'연결 종료: - {camera_id} {datetime.now() - connect_start_time}')
        pass

    



@router.websocket("/ai")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(deps.get_db)):
    """
    ai 요구사항만 맞춰서 실행
    병렬 처리 X
    버퍼 X - 파일로 저장 X
    단지 카메라 객체만 유지
    """
    # id, time
    connect_start_time = datetime.now()
    camera_id = str(uuid.uuid4())

    # 처음 접속 =  위병소 리스트 전달
    await websocket.accept()
    house_list = [data.house for data in get_guardhouse(db)]
    await websocket.send_json({
        'type' : "list",
        'list' : house_list,
    })

    print("소캣 연결 완료")
    omil_detecter = OmilZomil()
    
    # 수신 중
    print(" 이미지 수신 시작")
    try:
        while True:
            data = await websocket.receive_json()
            work_start = datetime.now()

            img = photo_2_img(data['photo'])
            cv2.imwrite(f"./image_list/{camera_id}_{work_start.strftime('%H-%M-%S')}.jpg", img)

            print(f'데이터 수신:- {camera_id}')
            report = omil_detecter.detect(img)
            print(report)
            print(report['step'])
            print(report.get('component'))

            msg = {
                'type' : "ai",
                'step' : report['step'],
                'component' : report.get('component'),
            }
            await websocket.send_json(msg)
            # 1차 처리 로그 출력
            print(f'테스크 1차 처리 완료: {camera_id} : {datetime.now() - work_start}')
            print()
            print()


    except WebSocketDisconnect:
        print(f'연결 종료: - {camera_id} {datetime.now() - connect_start_time}')
        pass


    
@router.websocket("/ping")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(deps.get_db)):
    """
    ai 요구사항만 맞춰서 실행
    병렬 처리 X
    버퍼 X - 파일로 저장 X
    단지 카메라 객체만 유지
    """
    # id, time
    connect_start_time = datetime.now()
    camera_id = str(uuid.uuid4())

    # 처음 접속 =  위병소 리스트 전달
    await websocket.accept()
    house_list = [data.house for data in get_guardhouse(db)]
    await websocket.send_json({
        'type' : "list",
        'list' : house_list,
    })

    print("소캣 연결 완료")
    
    # 수신 중
    print(" 이미지 수신 시작")
    try:
        while True:
            data = await websocket.receive_json()
            work_start = datetime.now()
            print(f'데이터 수신:- {camera_id}')
            msg = {
                'type' : "result",
                "kind" : "blue",
                "photo": data['photo'],
                'hair' : True,
                'nametag' : True,
                'leveltag' : True,
                'muffler' : True,
                'neck' : True,

            }
            await websocket.send_json(msg)
            # 1차 처리 로그 출력
            print(f'테스크 1차 처리 완료: {camera_id} : {datetime.now() - work_start}')
            print()
            print()


    except WebSocketDisconnect:
        print(f'연결 종료: - {camera_id} {datetime.now() - connect_start_time}')
        pass
