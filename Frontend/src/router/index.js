import { createRouter, createWebHistory } from "vue-router";
import LoginView from "../views/LoginView.vue";
import AppShell from "../views/AppShell.vue";
import AccountsView from "../views/AccountsView.vue";
import NewPaymentView from "../views/NewPaymentView.vue";
import InternalTransferView from "../views/InternalTransferView.vue";

function isAuthed() {
  return !!sessionStorage.getItem("token");
}

export const router = createRouter({
  history: createWebHistory(),
  routes: [
    {path: "/login", component: LoginView },
    {
      path: "/",
      component: AppShell,
      meta: { auth: true },
      children: [
        {path: "", redirect: "/accounts"},
        {path: "accounts", component: AccountsView},
        {path: "payments/new", component: NewPaymentView},
        {path: "transfers/internal", component: InternalTransferView}
      ],
    },
  ],
});

router.beforeEach((to) =>  {
  if (to.meta.auth && !isAuthed()) return "/login";
  if (to.path === "/login" && isAuthed()) return "/accounts";
});