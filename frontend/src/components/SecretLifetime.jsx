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

  const formatExpiration = (isoString) => {
    const utcTime = dayjs(isoString).format('YYYY-MM-DD HH:mm:ss [UTC]');
    const moscowTime = dayjs(isoString).add(3, 'hour').format('YYYY-MM-DD HH:mm:ss [MSK]');
    return `${utcTime} / ${moscowTime}`;
  };

  const calculateRemaining = (isoString) => {
    return dayjs(isoString).diff(dayjs(), 'second') + 10800;
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
            title="Expiration Date (UTC / MSK)"
            value={formatExpiration(expiresAt)}
          />
          <Statistic
            title="Remaining Time"
            value={`${calculateRemaining(expiresAt)} seconds`}
            valueStyle={{
              color: calculateRemaining(expiresAt) > 60 ? '#389e0d' : '#cf1322'
            }}
          />
        </div>
      )}
    </div>
  );
};

export default SecretLifetime;