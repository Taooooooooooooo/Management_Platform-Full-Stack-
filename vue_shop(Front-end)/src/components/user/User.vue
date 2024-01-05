<template>
  <div>
    <el-breadcrumb separator-class="el-icon-arrow-right">
      <el-breadcrumb-item :to="{ path: '/home' }">首页</el-breadcrumb-item>
      <el-breadcrumb-item>用户管理</el-breadcrumb-item>
      <el-breadcrumb-item>用户列表</el-breadcrumb-item>
    </el-breadcrumb>
    <el-card>
      <div>
        <el-row :gutter="20">
          <el-col :span="8">
            <el-input placeholder="请输入用户名" v-model="queryInfo.name">
              <el-button slot="append" icon="el-icon-search" @click="searchUser"></el-button>
            </el-input>
          </el-col>
          <el-col :span="2">
            <el-button
              type="primary"
              icon="el-icon-circle-plus-outline"
              @click="addDialogVisible = true"
            >新增用户</el-button>
          </el-col>
        </el-row>
        <el-row>
          <el-col>
            <el-table :data="userList" border style="width: 100%">
              <el-table-column type="index"></el-table-column>
              <el-table-column prop="id" label="ID"></el-table-column>
              <el-table-column prop="name" label="用户名"></el-table-column>
              <el-table-column prop="nick_name" label="昵称"></el-table-column>
              <el-table-column prop="email" label="邮箱"></el-table-column>
              <el-table-column prop="phone" label="电话"></el-table-column>
              <el-table-column prop="role_name" label="角色名称"></el-table-column>
              <el-table-column label="操作">
                <template slot-scope="scope">
                  <el-button type="primary" icon="el-icon-edit" circle @click="showEdit(scope.row)"></el-button>
                  <el-button
                    type="warning"
                    icon="el-icon-refresh"
                    circle
                    @click="showReset(scope.row)"
                  ></el-button>
                  <el-button type="danger" icon="el-icon-delete" circle @click="showDel(scope.row)"></el-button>
                </template>
              </el-table-column>
            </el-table>
          </el-col>
        </el-row>
        <el-pagination
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
          :current-page="queryInfo.pnum"
          :page-sizes="[1, 2, 5, 10]"
          :page-size="queryInfo.psize"
          layout="total, sizes, prev, pager, next, jumper"
          :total="total"
        ></el-pagination>
      </div>
    </el-card>
    <!-- 增加用户的窗口 -->
    <el-dialog
      title="新增用户"
      :visible.sync="addDialogVisible"
      width="30%"
      :before-close="addFormClose"
    >
      <el-form ref="addFormRef" :rules="addFormRules" :model="addForm" label-width="80px">
        <el-form-item label="账号" prop="name">
          <el-input v-model="addForm.name"></el-input>
        </el-form-item>
        <el-form-item label="昵称" prop="nick_name">
          <el-input v-model="addForm.nick_name"></el-input>
        </el-form-item>
        <el-form-item label="密码" prop="pwd">
          <el-input v-model="addForm.pwd"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="real_pwd">
          <el-input v-model="addForm.real_pwd"></el-input>
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="addForm.phone"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="addForm.email"></el-input>
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="addForm.role_name" placeholder="请选择角色">
            <el-option :label="r.name" :value="r.id" v-for="r in roles" :key='r.id'></el-option>
        </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="addFormClose">取 消</el-button>
        <el-button type="primary" @click="addUser">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 编辑用户窗口 -->
    <el-dialog
      title="编辑用户"
      :visible.sync="editDialogVisible"
      width="30%"
      :before-close="editFormClose"
    >
      <el-form ref="editFormRef" :rules="editFormRules" :model="editForm" label-width="80px">
        <el-form-item label="账号" prop="name">
          <el-input v-model="editForm.name" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="昵称" prop="nick_name">
          <el-input v-model="editForm.nick_name" :disabled="true"></el-input>
        </el-form-item>
        <el-form-item label="电话" prop="phone">
          <el-input v-model="editForm.phone"></el-input>
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="editForm.email"></el-input>
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="editForm.role_name" placeholder="请选择角色">
            <el-option :label="r.name" :value="r.id" v-for="r in roles" :key='r.id'></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="editDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="editUser">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 删除窗口 -->
    <el-dialog title="删除用户" :visible.sync="delDialogVisible" width="30%">
      <span>确认删除账户{{ delName }} 昵称 {{ delNickName}} 的用户吗？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="delDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="delUser">确 定</el-button>
      </span>
    </el-dialog>
    <!-- 重置密码窗口 -->
    <el-dialog title="重置用户密码" :visible.sync="resetDialogVisible" width="30%">
      <span>确认重置用户{{ resetName }} 昵称 {{ resetNickName}} 的密码吗？</span>
      <span slot="footer" class="dialog-footer">
        <el-button @click="resetDialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="resetUser">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>
<script>
export default {
  data() {
    const validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.addForm.pwd) {
        callback(new Error('两次输入密码不一致!'))
      } else {
        callback()
      }
    }
    const validatePhone = (rule, value, callback) => {
      // 定义一个正则来验证手机号是否是有效的
      const phoneReg = /^0?(13|14|15|18|17)[0-9]{9}$/
      if (phoneReg.test(value)) {
        return callback()
      }
      return callback(new Error('请输入有效的手机号'))
    }
    const validateEmail = (rule, value, callback) => {
      // 定义一个正则来验证邮箱是否是有效的
      const emailReg = /^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$/
      if (emailReg.test(value)) {
        return callback()
      }
      return callback(new Error('请输入有效的手机号'))
    }
    return {
      userList: [],
      queryInfo: {
        name: '',
        pnum: 1,
        psize: 2
      },
      total: 0,
      addDialogVisible: false,
      editDialogVisible: false,
      delDialogVisible: false,
      resetDialogVisible: false,
      addForm: {},
      editForm: {},
      delName: '',
      delNickName: '',
      delId: 0,
      resetName: '',
      resetNickName: '',
      resetId: 0,
      roles: [],
      addFormRules: {
        name: [
          { required: true, message: '请输入用户名', trigger: 'blur' },
          { min: 2, max: 5, message: '长度在 2~5 字符之间', trigger: 'blur' }
        ],
        nick_name: [
          { required: true, message: '请输入昵称', trigger: 'blur' },
          { min: 2, max: 5, message: '长度在 2~5 字符之间', trigger: 'blur' }
        ],
        pwd: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { min: 2, max: 5, message: '长度在 2~5 字符之间', trigger: 'blur' }
        ],
        real_pwd: [
          { required: true, message: '请输入密码', trigger: 'blur' },
          { validator: validatePass2, trigger: 'blur' }
        ],
        phone: [{ validator: validatePhone, trigger: 'blur' }],
        email: [{ validator: validateEmail, trigger: 'blur' }]
      },
      editFormRules: {
        phone: [{ validator: validatePhone, trigger: 'blur' }],
        email: [{ validator: validateEmail, trigger: 'blur' }]
      }
    }
  },
  created() {
    this.getUserList()
    this.getRole()
  },
  methods: {
    async getUserList() {
      const { data: res } = await this.$axios.get('/user/user_list', {
        params: this.queryInfo
      })
      if (res.status !== 200) return this.$msg.error(res.msg)
      this.total = res.data.totalPage
      this.userList = res.data.users
    },
    handleSizeChange(val) {
      this.queryInfo.psize = val
      this.getUserList()
    },
    handleCurrentChange(val) {
      this.queryInfo.pnum = val
      this.getUserList()
    },
    searchUser() {
      this.queryInfo.pnum = 1
      this.getUserList()
    },
    // 重置增加用户表单
    addFormClose() {
      this.$refs.addFormRef.resetFields()
      this.addDialogVisible = false
    },
    // 增加用户
    addUser() {
      // 发送请求之间，验证是数据是否规范
      this.$refs.addFormRef.validate(async valid => {
        if (!valid) return
        // 发送请求
        const { data: res } = await this.$axios.post(
          '/user/user',
          this.$qs.stringify(this.addForm)
        )
        // 验证结果
        if (res.status !== 200) return this.$msg.error(res.msg)
        this.$msg.success(res.msg)
        // 隐藏窗口
        this.addDialogVisible = false
        // 重置增加用户表单
        this.$refs.addFormRef.resetFields()
        // 重新获取用户列表
        this.getUserList()
      })
    },
    // 显示编辑用户窗口
    async showEdit(row) {
      // 发送请求，获取后台实时数据
      const { data: res } = await this.$axios.get('/user/user', {
        params: { id: row.id }
      })
      if (res.status !== 200) return this.$msg.error(res.msg)
      this.editForm = res.data
      // 显示窗口
      this.editDialogVisible = true
    },
    // 修改用户
    editUser() {
      this.$refs.editFormRef.validate(async valid => {
        if (!valid) return
        const { data: res } = await this.$axios.put(
          '/user/user',
          this.$qs.stringify(this.editForm)
        )
        if (res.status !== 200) return this.$msg.error(res.msg)
        this.$msg.success(res.msg)
        this.editDialogVisible = false
        // 重新获取下用户列表
        this.getUserList()
      })
    },
    // 显示删除窗口
    showDel(row) {
      this.delId = row.id
      this.delName = row.name
      this.delNickName = row.nick_name
      this.delDialogVisible = true
    },
    // 删除用户
    async delUser() {
      const { data: res } = await this.$axios.delete('/user/user', {
        data: { id: this.delId }
      })
      if (res.status !== 200) return this.$msg.error(res.msg)
      this.$msg.success(res.msg)
      this.delDialogVisible = false
      this.getUserList()
    },
    // 显示重置密码
    showReset(row) {
      this.resetId = row.id
      this.resetName = row.name
      this.resetNickName = row.nick_name
      this.resetDialogVisible = true
    },
    // 重置密码
    async resetUser() {
      const { data: res } = await this.$axios.get('/user/reset', {
        params: { id: this.resetId }
      })
      if (res.status !== 200) return this.$msg.error(res.msg)
      this.$msg.success(res.msg)
      this.resetDialogVisible = false
    },
    // 获取所有角色
    async getRole() {
      const { data: res } = await this.$axios.get('/role')
      if (res.status !== 200) return this.$msg.error(res.msg)
      this.roles = res.data
      console.log(this.roles)
    }
  }
}
</script>
<style scoped lang="less">
.el-table {
  margin-top: 10px;
}
</style>
