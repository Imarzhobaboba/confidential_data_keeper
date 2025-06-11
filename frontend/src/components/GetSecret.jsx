import React, { useState } from 'react';
import { Button, Form, Input, message } from 'antd';
import api from '../api';

const GetSecret = () => {
  const [form] = Form.useForm();
  const [secret, setSecret] = useState(null);
  const [loading, setLoading] = useState(false);

  const onFinish = async (values) => {
    setLoading(true);
    try {
      const result = await api.getSecret(values.access_key);
      setSecret(result.secret);
      message.success('Secret retrieved successfully!');
    } catch (error) {
      message.error(`Error: ${error.message}`);
      setSecret(null);
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
          <Input placeholder="Enter access key you received" />
        </Form.Item>

        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading}>
            Retrieve Secret
          </Button>
        </Form.Item>
      </Form>

      {secret && (
        <div style={{ marginTop: '20px' }}>
          <h4>Your Secret:</h4>
          <Input.TextArea 
            value={secret} 
            readOnly 
            rows={4} 
            style={{ backgroundColor: '#fffbe6' }} 
          />
          {/* <p style={{ color: '#ff4d4f', marginTop: '8px' }}>
            ⚠️ This secret has been deleted from our system and can no longer be accessed
          </p> */}
        </div>
      )}
    </div>
  );
};

export default GetSecret;