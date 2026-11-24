from datetime import datetime

import logging
from flask import g
from flask import request
from flask_restx import Resource

from auth_utils import get_client_ip, token_required
from extensions import db, ns
from models import Unit
from schemas import unit_model


@ns.route('/units')
class UnitList(Resource):
    @ns.marshal_list_with(unit_model)
    @ns.doc(security=None)
    def get(self):
        return Unit.query.all()

    @ns.expect(unit_model)
    @token_required
    def post(self):
        data = request.json or {}
        unit = Unit(
            type=data['type'],
            stage_code=data['stage_code'],
            title=data['title'],
            url=data['url'],
            cut_url=data['cut_url'],
            details=data['details'],
            img=data['img'],
            date=data['date']
        )
        db.session.add(unit)
        db.session.commit()

        logging.info(f'用户: {g.username} 添加unit记录: {data["title"]}，IP: {get_client_ip()}')
        return {'message': 'unit记录已添加'}, 201


@ns.route('/units/<int:id>')
class UnitItem(Resource):
    @ns.expect(unit_model)
    @token_required
    def put(self, id):
        data = request.json or {}
        unit = db.session.get(Unit, id)

        if not unit:
            return {'error': '找不到该unit记录'}, 404

        try:
            unit.type = data['type']
            unit.stage_code = data['stage_code']
            unit.title = data['title']
            unit.url = data['url']
            unit.cut_url = data['cut_url']
            unit.details = data['details']
            unit.img = data['img']
            unit.date = data['date']

            db.session.commit()

            logging.info(f'用户: {g.username} 更新unit记录: {data["title"]}，IP: {get_client_ip()}')
            return {'message': 'unit记录已更新'}, 200
        except (KeyError, ValueError) as error:
            return {'error': f'更新失败: {str(error)}'}, 400


@ns.route('/units/batch')
class UnitBatch(Resource):
    @ns.expect([unit_model])
    @token_required
    def post(self):
        data_list = request.json

        if not isinstance(data_list, list):
            return {'error': '请求体应为 JSON 数组'}, 400

        units = []
        for index, data in enumerate(data_list):
            try:
                unit = Unit(
                    type=data['type'],
                    stage_code=data['stage_code'],
                    title=data['title'],
                    url=data['url'],
                    cut_url=data['cut_url'],
                    details=data['details'],
                    img=data['img'],
                    date=data['date']
                )
                units.append(unit)
            except (KeyError, ValueError) as error:
                return {'error': f'第 {index + 1} 条数据有误: {str(error)}'}, 400

        db.session.add_all(units)
        db.session.commit()

        logging.info(f'用户: {g.username} 添加 {len(units)} 条unit记录，IP: {get_client_ip()}')
        return {'message': f'成功添加 {len(units)} 条unit记录'}, 201