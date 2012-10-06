Summary:	MooseFS - distributed, fault tolerant file system
Name:		mfs
Version:	1.6.26
Release:	0.3
License:	GPL v3
Group:		Daemons
Source0:	http://moosefs.com/tl_files/mfscode/%{name}-%{version}.tar.gz
# Source0-md5:	e49294bb9f2cbfff907ffed4f6662a37
URL:		http://www.moosefs.com/
BuildRequires:	libfuse-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		mfsconfdir	%{_sysconfdir}/%{name}

%description
MooseFS is an Open Source, easy to deploy and maintain, distributed,
fault tolerant file system for POSIX compliant OSes.

%package master
Summary:	MooseFS master server
Group:		Daemons

%description master
MooseFS master (metadata) server together with metarestore utility.

%package metalogger
Summary:	MooseFS metalogger server
Group:		Daemons

%description metalogger
MooseFS metalogger (metadata replication) server.

%package chunkserver
Summary:	MooseFS data server
Group:		Daemons

%description chunkserver
MooseFS data server.

%package client
Summary:	MooseFS client
Group:		Daemons

%description client
MooseFS client: mfsmount and mfstools.

%package cgi
Summary:	MooseFS CGI Monitor
Group:		Daemons
Requires:	python

%description cgi
MooseFS CGI Monitor.

%prep
%setup -q

%build
%configure \
	--sysconfdir=%{mfsconfdir} \
	--with-default-user=mfs \
	--with-default-group=mfs

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

for i in $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/*.dist; do
	mv $i $RPM_BUILD_ROOT/%{_sysconfdir}/%{name}/`basename $i .dist`;
done

%clean
rm -rf $RPM_BUILD_ROOT

%pre master
%groupadd -g 282 mfs
%useradd -u 282 -d /var/mfs -s /bin/false -c "MooseFS pseudo user" -g mfs mfs

%postun master
if [ "$1" = "0" ]; then
	%userremove mfs
	%groupremove mfs
fi

%files master
%defattr(644,root,root,755)
%doc NEWS README UPGRADE
%attr(755,root,root) %{_sbindir}/mfsmaster
%attr(755,root,root) %{_sbindir}/mfsmetadump
%attr(755,root,root) %{_sbindir}/mfsmetarestore
%{_mandir}/man5/mfsexports.cfg.5*
%{_mandir}/man5/mfstopology.cfg.5*
%{_mandir}/man5/mfsmaster.cfg.5*
%{_mandir}/man7/mfs.7*
%{_mandir}/man7/moosefs.7*
%{_mandir}/man8/mfsmaster.8*
%{_mandir}/man8/mfsmetarestore.8*
%attr(640,root,root) %config(noreplace) %{mfsconfdir}/mfsexports.cfg
%attr(640,root,root) %config(noreplace) %{mfsconfdir}/mfstopology.cfg
%attr(640,root,root) %config(noreplace) %{mfsconfdir}/mfsmaster.cfg
%attr(750,mfs,mfs) %dir %{_var}/mfs
%attr(640,mfs,mfs) %{_var}/mfs/metadata.mfs.empty

%files metalogger
%defattr(644,root,root,755)
%doc NEWS README UPGRADE
%attr(755,root,root) %{_sbindir}/mfsmetalogger
%{_mandir}/man5/mfsmetalogger.cfg.5*
%{_mandir}/man8/mfsmetalogger.8*
%attr(640,root,root) %config(noreplace) %{mfsconfdir}/mfsmetalogger.cfg
%attr(750,mfs,mfs) %dir %{_var}/mfs

%files chunkserver
%defattr(644,root,root,755)
%doc NEWS README UPGRADE
%attr(755,root,root) %{_sbindir}/mfschunkserver
%{_mandir}/man5/mfschunkserver.cfg.5*
%{_mandir}/man5/mfshdd.cfg.5*
%{_mandir}/man8/mfschunkserver.8*
%attr(640,root,root) %config(noreplace) %{mfsconfdir}/mfschunkserver.cfg
%attr(640,root,root) %config(noreplace) %{mfsconfdir}/mfshdd.cfg

%files client
%defattr(644,root,root,755)
%doc NEWS README UPGRADE
%attr(755,root,root) %{_bindir}/mfsappendchunks
%attr(755,root,root) %{_bindir}/mfscheckfile
%attr(755,root,root) %{_bindir}/mfsdeleattr
%attr(755,root,root) %{_bindir}/mfsdirinfo
%attr(755,root,root) %{_bindir}/mfsfileinfo
%attr(755,root,root) %{_bindir}/mfsfilerepair
%attr(755,root,root) %{_bindir}/mfsgeteattr
%attr(755,root,root) %{_bindir}/mfsgetgoal
%attr(755,root,root) %{_bindir}/mfsgettrashtime
%attr(755,root,root) %{_bindir}/mfsmakesnapshot
%attr(755,root,root) %{_bindir}/mfsmount
%attr(755,root,root) %{_bindir}/mfsrgetgoal
%attr(755,root,root) %{_bindir}/mfsrgettrashtime
%attr(755,root,root) %{_bindir}/mfsrsetgoal
%attr(755,root,root) %{_bindir}/mfsrsettrashtime
%attr(755,root,root) %{_bindir}/mfsseteattr
%attr(755,root,root) %{_bindir}/mfssetgoal
%attr(755,root,root) %{_bindir}/mfssettrashtime
%attr(755,root,root) %{_bindir}/mfssnapshot
%attr(755,root,root) %{_bindir}/mfstools
%{_mandir}/man1/mfsappendchunks.1*
%{_mandir}/man1/mfscheckfile.1*
%{_mandir}/man1/mfsdeleattr.1*
%{_mandir}/man1/mfsdirinfo.1*
%{_mandir}/man1/mfsfileinfo.1*
%{_mandir}/man1/mfsfilerepair.1*
%{_mandir}/man1/mfsgeteattr.1*
%{_mandir}/man1/mfsgetgoal.1*
%{_mandir}/man1/mfsgettrashtime.1*
%{_mandir}/man1/mfsmakesnapshot.1*
%{_mandir}/man1/mfsrgetgoal.1*
%{_mandir}/man1/mfsrgettrashtime.1*
%{_mandir}/man1/mfsrsetgoal.1*
%{_mandir}/man1/mfsrsettrashtime.1*
%{_mandir}/man1/mfsseteattr.1*
%{_mandir}/man1/mfssetgoal.1*
%{_mandir}/man1/mfssettrashtime.1*
%{_mandir}/man1/mfstools.1*
%{_mandir}/man7/mfs.7*
%{_mandir}/man7/moosefs.7*
%{_mandir}/man8/mfsmount.8*
%attr(640,root,root) %config(noreplace) %{mfsconfdir}/mfsmount.cfg

%files cgi
%defattr(644,root,root,755)
%doc NEWS README UPGRADE
%attr(755,root,root) %{_sbindir}/mfscgiserv
%{_mandir}/man8/mfscgiserv.8*
%{_datadir}/mfscgi