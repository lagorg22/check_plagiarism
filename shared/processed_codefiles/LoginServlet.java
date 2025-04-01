package login;
@WebServlet("/LoginServlet")
public class LoginServlet extends HttpServlet {
private static final long serialVersionUID = 1L;
public LoginServlet() {
super();
}
protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {}
protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
AccountManager am = (AccountManager)request.getServletContext().getAttribute(AccountManager.AM_NAME);
if (am.isCorrectPw(request.getParameter("name"), request.getParameter("pw"))) {
RequestDispatcher dispatch = request.getRequestDispatcher("welcome.jsp");
dispatch.forward(request, response);
} else {
RequestDispatcher dispatch = request.getRequestDispatcher("tryAgain.html");
dispatch.forward(request, response);
}
}
}