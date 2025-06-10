import React, { useState } from 'react';
import { Button, Form, Input, Statistic, message } from 'antd';
import dayjs from 'dayjs';
import api from '../api';

const SecretLifetime = () => {
  const [form] = Form.useForm();
  const [expiresAt, setExpiresAt] = useState(null);
  const [loading, setLoading] = useState(false);

  const onFinish = async (values) => {
    setLoading(true);
    try {
      const result = await api.getSecretLifetime(values.access_key);
      setExpiresAt(result.data);
      message.success('Lifetime retrieved successfully!');
    } catch (error) {
      message.error(`Error: ${error.message}`);
      setExpiresAt(null);
    } finally {
      setLoading(false);
    }
  };

  const formatExpiration = (dateString) => {
    const date = dayjs(dateString);
    return date.format('YYYY-MM-DD HH:mm:ss');
  };

  const calculateRemaining = (dateString) => {
    const now = dayjs();
    const expiration = dayjs(dateString);
    return expiration.diff(now, 'second');
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

        <Form.Item>
          <Button type="primary" htmlType="submit" loading={loading}>
            Check Lifetime
          </Button>
        </Form.Item>
      </Form>

      {expiresAt && (
        <div style={{ marginTop: '20px' }}>
          <Statistic
            title="Expiration Date"
            value={formatExpiration(expiresAt)}
            style={{ marginBottom: '16px' }}
          />
          
          <Statistic
            title="Remaining Time"
            value={`${calculateRemaining(expiresAt)} seconds`}
            valueStyle={{
              color: calculateRemaining(expiresAt) > 3600 ? '#389e0d' : '#cf1322'
            }}
          />
        </div>
      )}
    </div>
  );
};

export default SecretLifetime;