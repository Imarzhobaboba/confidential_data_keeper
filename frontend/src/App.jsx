import React, { useState } from 'react';
import { Tabs, Card, message } from 'antd';
import CreateSecret from './components/CreateSecret';
import GetSecret from './components/GetSecret';
import UpdateSecret from './components/UpdateSecret';
import DeleteSecret from './components/DeleteSecret';
import SecretLifetime from './components/SecretLifetime';

const App = () => {
  const [activeTab, setActiveTab] = useState('1');

  return (
    <div className="container">
      <h1 style={{ textAlign: 'center', marginBottom: '24px' }}>Secret Manager</h1>
      
      <Tabs
        activeKey={activeTab}
        onChange={setActiveTab}
        items={[
          { key: '1', label: 'Create Secret' },
          { key: '2', label: 'Get Secret' },
          { key: '3', label: 'Update Secret' },
          { key: '4', label: 'Delete Secret' },
          { key: '5', label: 'Check Lifetime' },
        ]}
      />

      <Card className="card">
        {activeTab === '1' && <CreateSecret />}
        {activeTab === '2' && <GetSecret />}
        {activeTab === '3' && <UpdateSecret />}
        {activeTab === '4' && <DeleteSecret />}
        {activeTab === '5' && <SecretLifetime />}
      </Card>
    </div>
  );
};

export default App;