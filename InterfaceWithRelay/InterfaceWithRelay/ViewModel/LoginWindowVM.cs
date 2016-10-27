using System;
using System.Threading.Tasks;

namespace InterfaceWithRelay.ViewModel
{
    class LoginWindowVM : NotifyPropertyChanged
    {
        #region MVVM model communication

        /// <summary>
        /// Reference to the views. 
        /// Do not use it anywhere before the initialization of windows.
        /// </summary>
        internal LoginPage loginPage;

        /*private Model model*/

        #endregion

        #region Properties

        private string loginName = "";
        public string LoginName
        {
            get { return loginName; }
            set { base.SetProperty(ref loginName, value); }
        }

        private string loginPassword = "";
        public string LoginPassword
        {
            get { return loginPassword; }
            set { base.SetProperty(ref loginPassword, value); }
        }

        private bool isLoggedIn = false;
        public bool IsLoggedIn
        {
            get { return isLoggedIn; }
            set { base.SetProperty(ref isLoggedIn, value); }
        }

        #endregion

        #region Constructor

        public LoginWindowVM(LoginPage page)
        {
            loginPage = page;

            LoginButtonCommand = new RelayCommand(loginButton_Execute, loginButton_CanExecute);
        }

        #endregion

        #region login button command

        public RelayCommand LoginButtonCommand { get; set; }

        private async void loginButton_Execute()
        {
            loginPage.progressBar.Start();
            await Task.Run(() =>
            {
                /// Fix this!
                System.Threading.Thread.Sleep(10000);

                IsLoggedIn = tryLoginFromVM();
#if DEBUG
                Console.WriteLine("Logged In!");
#endif
            });
            loginPage.progressBar.Stop();
            switchWindow();
        }

        private bool loginButton_CanExecute()
        {
            return (!string.IsNullOrEmpty(LoginName) && !string.IsNullOrEmpty(LoginPassword));
        }

        #endregion

        #region Login operation

        private bool tryLoginFromVM()
        {
            /// Fix this!
            return true;
        }
        #endregion

        private void switchWindow()
        {
            
        }
    }
}
