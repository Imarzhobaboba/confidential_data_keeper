import React, { useState } from 'react';
import { Button, Form, Input, InputNumber, message } from 'antd';
import api from '../api';

const UpdateSecret = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  const onFinish = async (values) => {
    setLoading(true);
    try {
      // Создаем объект только с заполненными полями
      const updateData = {
        secret: values.secret,
      };
      
      // Добавляем TTL только если он указан
      if (values.additional_ttl_seconds) {
        updateData.additional_ttl_seconds = values.additional_ttl_seconds;
      }

      const success = await api.updateSecret(values.access_key, updateData);
      
      if (success) {
        message.success('Secret updated successfully!');
        form.resetFields();
      }
    } catch (error) {
      if (error.response?.status === 422) {
        message.error(`Error: incorrect input`);
      }
      else {
        message.error(`Error: ${error.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Form form={form} layout="vertical" onFinish={onFinish}>
        <Form.Item
          name="access_key"
          label="Access Key"
          rules={[{ required: true, message: 'Please enter access key' }]}
        >
          <Input placeholder="Enter access key" />
        </Form.Item>

        <Form.Item
          name="secret"
          label="New Secret Value"
          // rules={[{ required: true, message: 'Please enter new secret' }]}
        >
          <Input.TextArea rows={4} placeholder="Enter new secret value" />
        </Form.Item>

        <Form.Item
          name="additional_ttl_seconds"
          label="Additional Lifetime (seconds)"
          tooltip="Optional: Extend the secret's lifetime"
        >
          <InputNumber min={1} style={{ width: '100%' }} />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading}>
            Update Secret
          </Button>
        </Form.Item>
      </Form>
    </div>
  );
};

export default UpdateSecret;